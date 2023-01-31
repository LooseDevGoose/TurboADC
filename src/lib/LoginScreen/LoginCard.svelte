<script>
import { getClient, Body} from '@tauri-apps/api/http';
import {navigate} from "svelte-routing";

let netscaler_ip = "";
let username = "";
let password = "";
let https_check = false;
let protocol;



async function create_session(){
    
        const client = await getClient();

        //Create body data for login 
        const data =  Body.json({
                    
                    login:{
                        username:username,
                        password:password
                    }
            
                }
            )
        //define protocol based on checkbox
        https_check ? protocol = "https" : protocol = "http"
        try{

         
        //POST request to login endpoint on NetScaler
        const response = await client.post(`${protocol}://${netscaler_ip}/nitro/v1/config/login`, data, {headers:{'Content-Type' : 'application/json'}} )

        //Get session ID data
        if(response.ok && response.data['sessionid']){
            setAuthCookie(response.data['sessionid']);
            navigate("/Dashboard")
        }else{
            alert(response.data.message)
        }
        }catch (error){
            alert(error)
        }
        



    };

//Create cookies with the input to use throughout the session
function setAuthCookie(token){
    document.cookie = `session_id = ${token}`
    document.cookie = `netscaler_ip = ${netscaler_ip}`
    document.cookie = `protocol = ${protocol}`
}


    



</script>

<main class="flex bg-dark-background h-screen w-screen items-center justify-center ">

<div class="w-96  bg-dark-foreground p-4 items-center align-middle shadow-xl rounded-xl hover:shadow-purple-900   ">
    
    <!--Logo-->
    <img src="/logo.png" height="125" width="125" alt="the turbo logo" class="m-auto"/>

    <!--Top layer-->
    <h1 class="text-gray-100 text-center font-bold text-2xl mt-6">Turbo Netscaler</h1>
    <h1 class="text-gray-400 text-center font-bold text-xs divide-x-2">v1.3.0</h1>

    <!--Divider-->
    <div class="w-full border-b border-gray-600 py-2"></div>
    
    <!--Input Fields-->
    <div class="relative mt-6">
        <input  bind:value={netscaler_ip} type="text"  class="block px-2 pb-2  w-full text-sm text-gray-200 font-mono bg-[#1d1d1d] rounded-lg border-1 appearance-none   dark:focus:border-purple-800 focus:outline-none focus:ring-0 focus:border-purple-800 peer" placeholder=" " />
        <label for="" class="absolute text-sm text-gray-400  duration-300 transform -translate-y-4 scale-75 top-2 z-10 origin-[0] px-2 font-bold peer-focus:px-2 peer-focus:text-gray-200 peer-focus:dark:text-blue-500 peer-placeholder-shown:scale-100 peer-placeholder-shown:-translate-y-1/2 peer-placeholder-shown:top-1/2 peer-focus:top-2 peer-focus:scale-75 peer-focus:-translate-y-4 left-1">Netscaler IP / FQDN</label>
    </div>

    <div class="relative mt-6">
        <input  bind:value={username} type="text"  class="block px-2 pb-2  w-full text-sm text-gray-200 font-mono bg-[#1d1d1d] rounded-lg border-1 appearance-none   dark:focus:border-purple-800 focus:outline-none focus:ring-0 focus:border-purple-800 peer" placeholder=" " />
        <label for="" class="absolute text-sm text-gray-400  duration-300 transform -translate-y-4 scale-75 top-2 z-10 origin-[0] px-2 font-bold peer-focus:px-2 peer-focus:text-gray-200 peer-focus:dark:text-blue-500 peer-placeholder-shown:scale-100 peer-placeholder-shown:-translate-y-1/2 peer-placeholder-shown:top-1/2 peer-focus:top-2 peer-focus:scale-75 peer-focus:-translate-y-4 left-1">Username</label>
    </div>
    
    <div class="relative mt-6">
        <input  bind:value={password} type="password" class="block px-2 pb-2  w-full text-sm text-gray-200 font-mono bg-[#1d1d1d] rounded-lg border-1 appearance-none   dark:focus:border-purple-800 focus:outline-none focus:ring-0 focus:border-purple-800 peer" placeholder=" " />
        <label for="" class="absolute text-sm text-gray-400  duration-300 transform -translate-y-4 scale-75 top-2 z-10 origin-[0] px-2 font-bold peer-focus:px-2 peer-focus:text-gray-200 peer-focus:dark:text-blue-500 peer-placeholder-shown:scale-100 peer-placeholder-shown:-translate-y-1/2 peer-placeholder-shown:top-1/2 peer-focus:top-2 peer-focus:scale-75 peer-focus:-translate-y-4 left-1">Password</label>
    </div>

    <!--HTTPS Checkbox-->

    <div class="flex items-center justify-center mb-4 mt-4  p-2  rounded-md ">
        <input  bind:checked={https_check} type="checkbox" class=" w-4 h-4 text-purple-600 bg-gray-100 rounded border-gray-300 focus:ring-purple-700 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600">
        <label for="" class="ml-2 text-sm font-medium text-gray-400 dark:text-gray-300">HTTPS</label>
    </div>

    <div class="flex items-center justify-center">
    <button on:click={create_session} class="block bg-purple-600 hover:bg-purple-800 p-2 rounded-md font-bold text-gray-200 min-w-full">Sign In</button>
    </div>

</div>
</main>