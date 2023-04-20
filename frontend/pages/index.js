import Head from 'next/head'
import Image from 'next/image'
import styles from '../styles/Home.module.css'
import { useEffect, useState } from 'react'
import Router, { useRouter } from "next/router";

export default function Home() {
  const router = useRouter();

  const [alldata, setalldata] = useState([])
  const [user_data, setuser] = useState(null)
  useEffect(() => {
    console.log(localStorage.getItem("token"))
    fetch("http://localhost:8000/get-subscription/", {
      method: "GET",
      headers: {
        "Authorization": "Token " + localStorage.getItem("token")
      }

    }).then((data) => data.json())
      .then((res) => {
        if (res.status === 200) {
          setalldata(res.data)
          console.log(localStorage.getItem('userid'))
          setuser(localStorage.getItem('userid'))
        } else {
          router.push("/signin")
        }
      })

  }, [])
  return (
    <>
      <div className='w-[1100px] mx-auto '>
        <div className='grid grid-cols-2 gap-4 mt-[60px]'>
          {alldata != undefined ? (<>
            {alldata.map((data) => (
              <>
                {data.subscription_items.map((item) => (
                  <>

                    {/* <div className='flex justify-center mt-[60px] gap-[40px]'> */}
                    <div className='border border-black w-[500px] mx-auto text-center rounded-[10px]  bg-white shadow-xl'>
                      <div className='w-[500px] mx-auto' >
                        <div className='mx-auto w-fit mt-10' >
                          <Image src={'/school-books.jpg'} width={150} height={100}></Image>
                        </div>
                        <div>
                          <label className='text-bold text-[20px]'>Subscription ID : </label>
                          <label className='text-bold text-[20px]'>{data.subscription_id}</label>
                        </div>
                        <div>
                          <label className='text-bold text-[20px]'>Item ID : </label>
                          <label className='text-bold text-[20px]'>{item.item_price_id}</label>
                        </div>
                        <form action={`${data.backend_url}/subscription/`} method='post'>
                          <input type='hidden' value='124'></input>
                          {/* <input type='hidden' name='item_price_id' value={"cbdemo_basic-INR-monthly"}></input> */}
                          <input type='hidden' name='item_price_id' value={item.item_price_id}></input>
                          <input type='hidden' name='user_id' value={user_data}></input>
                          {/* <input type='hidden' name='unit_price' value={"40000"}></input> */}
                          <input type='hidden' name='unit_price' value={item.amount}></input>
                          <p></p>
                          <div className='w-[150px] py-1 mx-auto bg-green-500 border mb-10 rounded-[4px] mt-10 shadow-xl' >
                            <button className=' '>{item.amount}/{data.billing_period_unit}</button>
                          </div>
                        </form>
                      </div>
                    </div>
                  </>

                ))}
              </>
            ))}
          </>
          ) : null}
        </div >
      </div>
    </>
  )
}
