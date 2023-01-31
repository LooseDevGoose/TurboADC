<script>
import { getClient, Body} from '@tauri-apps/api/http';
//Cookie data
const auth = ('; '+document.cookie).split(`; session_id=`).pop().split(';')[0];
const netscaler_ip = ('; '+document.cookie).split(`; netscaler_ip=`).pop().split(';')[0];
const protocol = ('; '+document.cookie).split(`; protocol=`).pop().split(';')[0];

export let title = "";
export let icon = "";


//Create a new SSL profile
async function save_nsconfig(){   
    const client = await getClient();
    const data =  Body.json({

        nsconfig: {}
    }
            )
        //POST request to login endpoint on NetScaler
    const response = await client.post(`${protocol}://${netscaler_ip}/nitro/v1/config/nsconfig?action=save`, data, {headers:{'Content-Type' : 'application/json', 'Cookie' : `NITRO_AUTH_TOKEN=${auth}`}} )

    if(response.ok){

    //assign data to variable for HTML useage
    let response_data = await response.data
    console.log(response_data)
    alert("Configuration Saved!")
  }else{
    alert("Something went wrong :(\n" + "Error:  \n" + response.data.message)
  }
    console.log(response)
}

</script>


<main>
<!--Title Card-->
<div class="flex justify-between bg-dark-foreground items-center px-4 rounded-md ">
    <div class="flex items-center">
        <img height='64' width='64' src={icon} alt="Menu top Icon"/>
        <h1 class="text-gray-100 text-4xl font-bold px-6 py-6 truncate">{title}</h1>     
    </div>
    <div class="md:mr-4">
        <button on:click={() => save_nsconfig()} class="group  bg-lime-500 hover:bg-green-600 text-gray-800 font-bold py-2 px-4 rounded inline-flex items-center">
            <svg class="group-hover:animate-bounce fill-current w-4 h-4 mr-2" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M13 8V2H7v6H2l8 8 8-8h-5zM0 18h20v2H0v-2z"/></svg>
            <span class="appearance-none truncate">Save Config</span>
        </button>
    </div>
</div>

</main>