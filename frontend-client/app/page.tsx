import React from "react";
import Head from "next/head";

const menuItems = [
  { name: "Pav Bhaji", image: "/images/pav-bhaji.jpg" },
  { name: "Chole Bhature", image: "/images/chole_bhature.jpg" },
  { name: "Mango Lassi", image: "/images/mango-lassi.jpg" },
  { name: "Pizza", image: "/images/pizza.jpg" },
  { name: "Vada Pav", image: "/images/vada-pav.jpg" },
  { name: "Biryani", image: "/images/biryani.jpg" },
  { name: "Masala Dosa", image: "/images/Masala-Dosa.jpg" },
  { name: "Rava Dosa", image: "/images/Rava-Dosa.jpg" },
  { name: "Samosa", image: "/images/Samosa.jpg" },
];

export default function Home() {
  return (
    <>
      <Head>
        <title>Eatery - Fast Food Restaurant</title>
        <meta name="description" content="Best fast food in NYC! Order now from Eatery." />
      </Head>

      <div className="min-h-screen bg-gray-100 text-gray-900">
        {/* Hero Section */}
        <header className="bg-yellow-500 text-white text-center py-20">
          <h1 className="text-6xl font-extrabold drop-shadow-lg">Welcome to Eatery</h1>
          <p className="text-2xl mt-4 font-semibold">The Best Fast-Food in NYC!</p>
          <button className="mt-6 bg-white text-yellow-500 px-8 py-3 rounded-xl text-lg font-bold shadow-md hover:bg-yellow-100 transition-all duration-300">
            Order Now
          </button>
        </header>

        {/* Menu Section */}
        <section className="py-16 px-6 md:px-16">
          <h2 className="text-5xl font-bold text-center mb-10">🍽 Our Menu</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-10">
            {menuItems.map((item, index) => (
              <div
                key={index}
                className="bg-white rounded-xl shadow-lg overflow-hidden transform transition-all duration-300 hover:scale-105"
              >
                <img src={item.image} alt={item.name} className="w-full h-56 object-cover" />
                <div className="p-4 text-center">
                  <h3 className="text-3xl font-semibold">{item.name}</h3>
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* Location Section */}
        <section className="bg-gray-200 py-16 text-center">
          <h2 className="text-5xl font-bold">📍 Visit Us in NYC</h2>
          <p className="text-2xl mt-4 font-medium">123 Food Street, New York City, NY</p>
        </section>

        {/* Floating Chatbot */}
        <div className="fixed bottom-4 right-4 shadow-lg">
          <iframe width="350" height="430" allow="microphone;"
                  src="https://console.dialogflow.com/api-client/demo/embedded/995d042d-e965-4d40-88b4-d5e66c03ca44"></iframe>
        </div>

        {/* Footer */}
        <footer className="bg-gray-900 text-white text-center py-8">
          <p className="text-lg">&copy; 2024 Eatery. All rights reserved.</p>
        </footer>
      </div>
    </>
  );
}
