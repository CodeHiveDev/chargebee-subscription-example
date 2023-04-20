import React from "react";
import Image from "next/image";
import { useState, useContext, useEffect } from "react";
import Link from "next/link";
import Router, { useRouter } from "next/router";
import { EnvelopeIcon, LockClosedIcon, XCircleIcon, UserIcon } from "@heroicons/react/24/outline";
import { backend_api } from "../components/api";
function Signin() {
    //google login for SSO
    const router = useRouter();
    const [open, setOpen] = useState(false);
    const [email, setEmail] = useState();
    const [password, setPassword] = useState();

    const [messageshow, setshowmessage] = useState(false);
    const [greenmsg, setGreenmsg] = useState(false);

    //error pop up show
    useEffect(() => {
        if (messageshow === true) {
            var message_tag = document.getElementById("credetion-not-found");
            if (message_tag) {
                message_tag.addEventListener("click", function () {
                    setshowmessage(false);
                });
            }
        }
    }, [messageshow]);

    //sucess popup show
    useEffect(() => {
        if (greenmsg === true) {
            var message_tag = document.getElementById("credetion-green-not-found");
            if (message_tag) {
                message_tag.addEventListener("click", function () {
                    setGreenmsg(false);
                });
            }
        }
    }, [greenmsg]);

    //fetch data to backend
    const Submit_Form = () => {
        if (email !== undefined && email !== "") {
            if (password !== undefined && password !== "") {
                var user = document.getElementById("email-address").value;
                var pwd = document.getElementById("password").value;
                var first_name = document.getElementById("first_name").value;
                var last_name = document.getElementById("last_name").value;
                var credentials = {
                    email: user,
                    password: pwd,
                    first_name: first_name,
                    last_name: last_name,
                };

                return fetch(backend_api + "/accounts/signup/", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify(credentials),
                })
                    .then((data) => data.json())

                    .then((res) => {
                        if (res.status == 201) {

                            router.push("/signin");

                        } else {
                            alert(res.message);
                        }
                    });
            } else {
                alert("please check password")
            }
        } else {
            alert("Enter Email Id")
        }
    };







    return (
        <div>

            <div className="flex py-4 h-screen  flex flex-col justify-center -mt-5">
                <div className="border px-8 md:px-12 py-5 w-fit mx-auto rounded-lg">

                    <div className="w-fit mx-auto text-lg font-bold">
                        <h2>Chargebee Subscription</h2>
                    </div>
                    <div className="w-fit text-gray-500 mx-auto text-xs ">
                        signin to continue
                    </div>
                    <div className="py-3">
                        <div className="w-fit  mx-auto">
                            <fieldset className="w-[180px] md:w-full flex items-center  border rounded  border-gray-400">
                                <legend className="ml-5 text-sm text-gray-600">First Name</legend>
                                <UserIcon className="h-8 pl-2 pr-2 pb-2   text-gray-500" />
                                <input
                                    id="first_name"
                                    onChange={(e) => {
                                        setEmail(e.target.value);
                                    }}
                                    name="first_name"
                                    type="text"
                                    autoComplete="first_name"
                                    required
                                    className="h-8 w-[200px] lg:w-[250px] text-sm text-gray-800 pl-2 pr-2 pb-2 rounded-lg focus:outline-none focus:ring-[#ff7a43] focus:border-[#ff7a43]"
                                />
                            </fieldset>
                        </div>
                    </div>
                    <div className="py-3">
                        <div className="w-fit  mx-auto">
                            <fieldset className="w-[180px] md:w-full flex items-center  border rounded  border-gray-400">
                                <legend className="ml-5 text-sm text-gray-600">Last Name</legend>
                                <UserIcon className="h-8 pl-2 pr-2 pb-2   text-gray-500" />
                                <input
                                    id="last_name"
                                    onChange={(e) => {
                                        setEmail(e.target.value);
                                    }}
                                    name="Last Name"
                                    type="text"
                                    autoComplete="Last Name"
                                    required
                                    className="h-8 w-[200px] lg:w-[250px] text-sm text-gray-800 pl-2 pr-2 pb-2 rounded-lg focus:outline-none focus:ring-[#ff7a43] focus:border-[#ff7a43]"
                                />
                            </fieldset>
                        </div>
                    </div>
                    <div className="py-3">
                        <div className="w-fit  mx-auto">
                            <fieldset className="w-[180px] md:w-full flex items-center  border rounded  border-gray-400">
                                <legend className="ml-5 text-sm text-gray-600">E-mail</legend>
                                <EnvelopeIcon className="h-8 pl-2 pr-2 pb-2   text-gray-500" />
                                <input
                                    id="email-address"
                                    onChange={(e) => {
                                        setEmail(e.target.value);
                                    }}
                                    name="email"
                                    type="email"
                                    autoComplete="email"
                                    required
                                    className="h-8 w-[200px] lg:w-[250px] text-sm text-gray-800 pl-2 pr-2 pb-2 rounded-lg focus:outline-none focus:ring-[#ff7a43] focus:border-[#ff7a43]"
                                />
                            </fieldset>
                        </div>
                    </div>

                    <div className="py-3">
                        <div className="w-fit  mx-auto">
                            <fieldset className="w-[180px] md:w-full flex items-center  border rounded  border-gray-400">
                                <legend className="ml-5 text-sm text-gray-600">Password</legend>
                                <LockClosedIcon className="h-8 pl-2 pr-2 pb-2   text-gray-500" />
                                <input
                                    onChange={(e) => setPassword(e.target.value)}
                                    id="password"
                                    name="password"
                                    type="password"
                                    autoComplete="password"
                                    required
                                    className="h-8 w-[200px] lg:w-[250px] text-sm text-gray-800 pl-2 pr-2 pb-2 rounded-lg focus:outline-none focus:ring-[#ff7a43] focus:border-[#ff7a43]"
                                />
                            </fieldset>
                        </div>
                    </div>

                    <div
                        id="passoword-error"
                        className="ml-2 block text-sm text-red-600"
                    ></div>



                    <div className="w-fit  mx-auto pt-6 pb-3">
                        <button
                            onClick={() => Submit_Form()}
                            className="transform cursor-pointer transition duration-500 hover:scale-[1.05] hover:text-[16px] border w-[240px] lg:w-[292px] px-3 py-2.5 rounded-lg bg-[#021B41]  text-white font-bold"
                        >
                            {" "}
                            Sign In{" "}
                        </button>
                    </div>
                    <hr className="border-b mb-4 border-gray-100 mx-auto w-[240px] lg:w-[280px]" />
                </div>
            </div>

        </div>
    );
}

export default Signin;
