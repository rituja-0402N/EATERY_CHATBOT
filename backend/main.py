from fastapi import FastAPI,Request
from starlette.responses import JSONResponse
from backend import db_helper, helper

app = FastAPI()
inprogress_orders={}
@app.post("/")
async def handle_request(request: Request):
    payload = await request.json()

    intent = payload['queryResult']['intent']['displayName']
    parameter = payload['queryResult']['parameters']
    output_contexts = payload['queryResult']['outputContexts']
    print("Intent:", intent)
    session_id = helper.extract_session_id(output_contexts[0]['name'])
    intent_handler_dict = {
        "track.order - context : ongoing-tracking" : track_order,
        "order.complete - context: ongoing-order" : complete_order,
        "order.add - context: ongoing-order" : add_to_order,
        "order.remove - context: ongoing-order": remove_from_order
    }
    return intent_handler_dict[intent](parameter,session_id)




def add_to_order(parameter:dict,session_id:str):
    food_items = parameter.get('food-item', [])
    quantities = parameter.get('number', [])

    print("food items:", food_items, "quantities:", quantities)
    if len(food_items) != len(quantities):
        fullfillment_text = " Sorry I didn't understand. Can you please specify food items and quantity"
    else:
        new_food_dict = dict(zip(food_items,quantities))
        if session_id in inprogress_orders:
            current_food_dict = inprogress_orders[session_id]
            current_food_dict.update(new_food_dict)
            inprogress_orders[session_id] = current_food_dict
        else:
            inprogress_orders[session_id] = new_food_dict
        order_str = helper.get_str_from_food_dict(inprogress_orders[session_id])
        print(session_id,"session order:", inprogress_orders)
        fullfillment_text = f"So far you have: {order_str}. Do you need anything else?"
    return JSONResponse(content={
        "fulfillmentText": fullfillment_text
    })

def complete_order(parameter:dict,session_id:str):
    if session_id not in inprogress_orders:
        fullfillment_text = "I'm trouble finding your order. Sorry! Can you place a new order?"
    else:
        order = inprogress_orders[session_id]
        order_id = save_db(order)
        if order_id == -1:
            fullfillment_text = "Sorry, I couldnt place your order. Please place a new order"
        else:
            order_total = db_helper.get_total_order_price(order_id)
            fullfillment_text = (f"Awesome! We have placed your order."\
                                  f"Your order is {order_total}."\
                                 f"Your order_id is {order_id}")

            #delete the current session
            del inprogress_orders[session_id]
            return JSONResponse(content={
                "fulfillmentText": fullfillment_text
            })

def remove_from_order(parameter:dict,session_id:str):
    if session_id not in inprogress_orders:
        return JSONResponse(content={
            "fullfillment": f"Sorry, I couldnt find your order. Please place a new order."
        })
    current_dict = inprogress_orders[session_id]
    food_items = parameter.get('food-item', [])
    removed_item = []
    no_such_items = []
    for item in food_items:
        if item not in current_dict:
            no_such_items.append(item)
            return JSONResponse(content={
                "fullfillment": f"Sorry, I couldnt find your item."
            })
        else:
            removed_item.append(item)
            del current_dict[item]
        if len(removed_item) > 0:
            fullfillment_text =  f"Removed {", ".join(removed_item)} items from your order!"
        if len(no_such_items) > 0:
            fullfillment_text = f"Your current order doesnt have {", ".join(no_such_items)}"
        if len(current_dict.keys()) == 0:
            fullfillment_text += f"Your order is empty!"
        else:
            order_str = helper.get_str_from_food_dict(current_dict)
            fullfillment_text = f"The items in your order are {order_str}"
        return JSONResponse(content={
            "fulfillmentText": fullfillment_text
        })


def save_db(order:dict):
    next_order_id = db_helper.get_next_order_id()
    for food_item, quantity in order.items():
        rcode = db_helper.insert_order_item(food_item, quantity, next_order_id)
        if rcode == -1:
            return -1
    db_helper.insert_order_tracking(next_order_id, "inprogress")
    return next_order_id

def track_order(parameter: dict,session_id:str):
    order_id = int(parameter['number'])
    print("Order ID:", order_id)
    order_status = db_helper.get_order_status(order_id)
    if order_status:
        print("Order Status:", order_status)
        fullfillment = f"The order {order_id} has been fulfilled is {order_status}."
    else:
        fullfillment = f"No order has been found with {order_id}."

    return JSONResponse(content={
        "fulfillmentText": fullfillment
    })
