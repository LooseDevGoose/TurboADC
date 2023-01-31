<script>
import logo from "/logo.png"
import {navigate} from "svelte-routing";
import { getClient, Body} from '@tauri-apps/api/http';

const auth = ('; '+document.cookie).split(`; session_id=`).pop().split(';')[0];
const netscaler_ip = ('; '+document.cookie).split(`; netscaler_ip=`).pop().split(';')[0];
const protocol = ('; '+document.cookie).split(`; protocol=`).pop().split(';')[0];

async function logout(){   
    const client = await getClient();
    const data =  Body.json({

        logout: {
         sessionid: `${auth}`
        }
    }
            )
        //POST request to login endpoint on NetScaler
    const response = await client.delete(`${protocol}://${netscaler_ip}/nitro/v1/config/logout`, data, {headers:{'Content-Type' : 'application/json', 'Cookie' : `NITRO_AUTH_TOKEN=${auth}`}} )

    if(response.ok){

    //assign data to variable for HTML useage
    let response_data = await response.data
    console.log(response_data)
    alert("Logged out of your session!")
    //refresh feed
  }else{
    alert("Something went wrong :(\n" + "Error:  \n" + response.data.message)
  }
    console.log(response)
}
</script>

<main>
    <aside class="w-52 sticky top-0" aria-label="Sidebar">
        <div class="h-screen py-4 px-3 bg-dark-foreground  shadow-black shadow-xl ">

         <!--Logo & Subtext-->
            <div class="flex  justify-center overflow-clip">
               <img src={logo} height="120" width="120" alt="Goose Logo" class="m-auto"/>
            </div>   
            <h1 class="font-medium text-sm text-gray-300 block text-center mt-4">Turbo Netscaler v1.3.0</h1>
            <hr class="my-4 h-px bg-gray-600 border-0">
         <!--List of buttons-->
         <ul class="space-y-3 ">
            <!--Dashboard-->
              <li>
                 <a href="/Dashboard" class="flex items-center p-2 text-base font-bold text-gray-300 rounded-lg dark:text-white hover:bg-gray-600">
                    <svg aria-hidden="true" class="w-6 h-6 text-gray-500 transition duration-75 dark:text-gray-400 group-hover:text-gray-900 dark:group-hover:text-white" fill="#9333ea" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path d="M2 10a8 8 0 018-8v8h8a8 8 0 11-16 0z"></path><path d="M12 2.252A8.014 8.014 0 0117.748 8H12V2.252z"></path></svg>
                    <span class="ml-3">Dashboard</span>
                 </a>
              </li>
              <!--SSL Profiles-->
              <li>
                  <a href="/SSL_Profiles" class="flex items-center p-2 text-base font-bold text-gray-300 rounded-lg dark:text-white hover:bg-gray-600">
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#9333ea" class="w-6 h-6">
                     <path fill-rule="evenodd" d="M12.516 2.17a.75.75 0 00-1.032 0 11.209 11.209 0 01-7.877 3.08.75.75 0 00-.722.515A12.74 12.74 0 002.25 9.75c0 5.942 4.064 10.933 9.563 12.348a.749.749 0 00.374 0c5.499-1.415 9.563-6.406 9.563-12.348 0-1.39-.223-2.73-.635-3.985a.75.75 0 00-.722-.516l-.143.001c-2.996 0-5.717-1.17-7.734-3.08zm3.094 8.016a.75.75 0 10-1.22-.872l-3.236 4.53L9.53 12.22a.75.75 0 00-1.06 1.06l2.25 2.25a.75.75 0 001.14-.094l3.75-5.25z" clip-rule="evenodd" />
                   </svg>
                    
                  <span class="flex-1 ml-3 whitespace-nowrap">SSL Profiles</span>
                 </a>
              </li>

            <!--SSL Certificates-->
              <!-- <li>
               <a href="/SSL_Profiles" class="flex items-center p-2 text-base font-bold text-gray-300 rounded-lg dark:text-white hover:bg-gray-600">
               <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#9333ea" class="w-6 h-6">
                     <path fill-rule="evenodd" d="M4.5 3.75a3 3 0 00-3 3v10.5a3 3 0 003 3h15a3 3 0 003-3V6.75a3 3 0 00-3-3h-15zm4.125 3a2.25 2.25 0 100 4.5 2.25 2.25 0 000-4.5zm-3.873 8.703a4.126 4.126 0 017.746 0 .75.75 0 01-.351.92 7.47 7.47 0 01-3.522.877 7.47 7.47 0 01-3.522-.877.75.75 0 01-.351-.92zM15 8.25a.75.75 0 000 1.5h3.75a.75.75 0 000-1.5H15zM14.25 12a.75.75 0 01.75-.75h3.75a.75.75 0 010 1.5H15a.75.75 0 01-.75-.75zm.75 2.25a.75.75 0 000 1.5h3.75a.75.75 0 000-1.5H15z" clip-rule="evenodd" />
                </svg>
                 
               <span class="flex-1 ml-3 whitespace-nowrap">Certificates</span>
              </a>
           </li> -->
                 <br>
                 <hr class="my-4 border-gray-600 border-1">
           <!--Logout-->
                   <li class="bottom-0">
                     <a on:click={() => logout()}  class="flex items-center p-2 text-base font-bold text-gray-300 rounded-lg dark:text-white hover:bg-gray-600">
                     <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#9333ea" class="w-6 h-6">
                        <path d="M10.375 2.25a4.125 4.125 0 100 8.25 4.125 4.125 0 000-8.25zM10.375 12a7.125 7.125 0 00-7.124 7.247.75.75 0 00.363.63 13.067 13.067 0 006.761 1.873c2.472 0 4.786-.684 6.76-1.873a.75.75 0 00.364-.63l.001-.12v-.002A7.125 7.125 0 0010.375 12zM16 9.75a.75.75 0 000 1.5h6a.75.75 0 000-1.5h-6z" />  </svg>
                       
                     <span class="flex-1 ml-3 whitespace-nowrap">Logout</span>
                    </a>
                 </li>
       
           </ul>
   
        </div>
     </aside>

</main>