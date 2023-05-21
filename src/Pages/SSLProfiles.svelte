<script>
import { getClient, Body} from '@tauri-apps/api/http';
import { onMount } from 'svelte';
import NavBar from '../lib/General/NavBar.svelte';
import SSLCard from '../lib/SSL_Profiles/SSLCard.svelte';
import PageTitleCard from '../lib/General/PageTitleCard.svelte';
import SSL_Profiles_Icon from '../../public/Icons/SSL_Profiles_Icon.svg';
import SSLProfileTable from '../lib/SSL_Profiles/SSLProfileTable.svelte';
import SSLServersTable from '../lib/SSL_Profiles/SSLServersTable.svelte';
import { Button, Modal} from 'flowbite-svelte';


//Cookie data
const auth = ('; '+document.cookie).split(`; session_id=`).pop().split(';')[0];
const netscaler_ip = ('; '+document.cookie).split(`; netscaler_ip=`).pop().split(';')[0];
const protocol = ('; '+document.cookie).split(`; protocol=`).pop().split(';')[0];

//Bindings for Components
let server_list = [];
let ciphergroup_list = [];
let ssl_profile_list;
let ssl_counters;


//Modal Variables for open/closing

//Modal for new SSL profile
let modal_new_ssl_profile = false;

//Modal to edit SSL profile
let modal_edit_ssl_profile = false;


//Default values for SSL profile, this is used upon creation
let default_data = {

      name: "Turbo_Netscaler_SSLProfile",
      sslprofiletype: "FrontEnd",
      ssllogprofile : null,
      dhcount : null,
      dh : "DISABLED",
      dhfile : null,
      ersa : "ENABLED",
      ersacount : "0",
      sessreuse : "ENABLED",
      sesstimeout : "120",
      cipherredirect : "DISABLED",
      cipherurl : null,
      clientauth : "DISABLED",
      clientcert : null,
      dhkeyexpsizelimit : "DISABLED",
      sslredirect : "DISABLED",
      redirectportrewrite : "DISABLED",
      ssl3 : "DISABLED",
      tls1 : "DISABLED",
      tls11 : "DISABLED",
      tls12 : "ENABLED",
      tls13 : "DISABLED",
      snienable : "DISABLED",
      ocspstapling : "DISABLED",
      serverauth : "DISABLED",
      commonname : null,
      pushenctrigger : "Always",
      sendclosenotify : "YES",
      cleartextport : "0",
      insertionencoding : "Unicode",
      denysslreneg : "NONSECURE",
      quantumsize : "8192",
      strictcachecks : "NO",
      encrypttriggerpktcount : "45",
      pushflag : "0",
      dropreqwithnohostheader : "NO",
      snihttphostmatch : "CERT",
      pushenctriggertimeout : "1",
      ssltriggertimeout : "100",
      clientauthuseboundcachain : "DISABLED",
      sslinterception : "DISABLED",
      sslireneg : "ENABLED",
      ssliocspcheck : "ENABLED",
      sslimaxsessperserver : "10",
      sessionticket : "DISABLED",
      sessionticketlifetime : "300",
      sessionticketkeyrefresh : "ENABLED",
      sessionticketkeydata : null,
      sessionkeylifetime : "3000",
      prevsessionkeylifetime : "0",
      hsts : "ENABLED",
      maxage : "15552000",
      includesubdomains : "YES",
      preload : "YES",
      skipclientcertpolicycheck : "DISABLED",
      zerorttearlydata : "DISABLED",
      tls13sessionticketsperauthcontext : "1",
      dhekeyexchangewithpsk : "NO",
      allowextendedmastersecret : "NO",
      alpnprotocol : null
}


//Actual values of a virtual servers to edit, this is used for updates (edits)
let imported_data = {    
}

//Create a new SSL profile
async function create_ssl_profile(){   
    const client = await getClient();

    const data =  Body.json({

        sslprofile: default_data
    }
            )
        //POST request to login endpoint on NetScaler
    const response = await client.post(`${protocol}://${netscaler_ip}/nitro/v1/config/sslprofile`, data, {headers:{'Content-Type' : 'application/json', 'Cookie' : `NITRO_AUTH_TOKEN=${auth}`}} )

    if(response.ok){

    //assign data to variable for HTML useage
    let response_data = await response.data
    console.log(response_data)
    alert("Profile Created!")
    //refresh feed
    get_sslprofiles()
  }else{
    alert("Something went wrong :(\n" + "Error:  \n" + response.data.message)
  }
    console.log(response)
}


//Get all active servers based on SSL (inc gateway/gslb etc)
async function get_sslvserver_data(){

    const client = await getClient();
           
            //POST request to login endpoint on NetScaler
      const response = await client.get(`${protocol}://${netscaler_ip}/nitro/v1/config/sslvserver`, {headers:{'Content-Type' : 'application/json', 'Cookie' : `NITRO_AUTH_TOKEN=${auth}`}} )

      if(response.ok){

        //assign data to variable for HTML useage
        server_list= await response.data
        //reformat data for easier use
        server_list = server_list.sslvserver
      }

}

//Get all SSL Profiles present on the Netscaler
async function get_sslprofiles(){

    const client = await getClient();
           
            //POST request to login endpoint on NetScaler
      const response = await client.get(`${protocol}://${netscaler_ip}/nitro/v1/config/sslprofile`, {headers:{'Content-Type' : 'application/json', 'Cookie' : `NITRO_AUTH_TOKEN=${auth}`}} )

      if(response.ok){

        //assign data to variable for HTML useage
        ssl_profile_list = await response.data
        //reformat data for easier use
        ssl_profile_list = ssl_profile_list.sslprofile
      }
}

//Get all Cipher Suits present on the Netscaler
async function get_ciphergroups(){

    const client = await getClient();
           
            //POST request to login endpoint on NetScaler
      const response = await client.get(`${protocol}://${netscaler_ip}/nitro/v1/config/sslcipher`, {headers:{'Content-Type' : 'application/json', 'Cookie' : `NITRO_AUTH_TOKEN=${auth}`}} )

      if(response.ok){

        //assign data to variable for HTML useage
        ciphergroup_list = await response.data
        //reformat data for easier use
        ciphergroup_list = ciphergroup_list.sslcipher
      }
}

//Get all active SSL sessions 
async function get_sslvserver_counters(){

    const client = await getClient();
           
            //POST request to login endpoint on NetScaler
      const response = await client.get(`${protocol}://${netscaler_ip}/nitro/v1/stat/ssl`, {headers:{'Content-Type' : 'application/json', 'Cookie' : `NITRO_AUTH_TOKEN=${auth}`}} )

      if(response.ok){

        //assign data to variable for HTML useage
        ssl_counters = await response.data
        //reformat data for easier use
        ssl_counters = ssl_counters.ssl
        
      }
}


//List of API calls that need to be made upon initialization of page
function prescript(){
    get_sslvserver_data()
    get_sslprofiles()
    get_ciphergroups()
    get_sslvserver_counters()
}

//Start all the required API calls on mount
onMount(async () => prescript()) 

</script>

<main class="bg-[#222222] h-full w-full">
    <div class="flex">
    <NavBar/>
        
        <!--Main container (right side)-->
        <div class="px-20 py-12 max-w-full max-h-full">
         <PageTitleCard title="SSL Profiles" icon={SSL_Profiles_Icon}/>

              <!--First layer of cards -> 4 horizontal--> 
            <div class="grid gap-4 justify-between grid-cols-5">
                {#if ssl_counters}
                <SSLCard title="SSLV3 Rate/s" metric_value={ssl_counters.ssltotsslv3sessionsrate} />
                <SSLCard title="TLS1.0 Rate/s"  metric_value={ssl_counters.ssltottlsv1sessionsrate}/>
                <SSLCard title="TLS1.1 Rate/s"  metric_value={ssl_counters.ssltottlsv11sessionsrate} />
                <SSLCard title="TLS1.2 Rate/s" secure_cipher={true}  metric_value={ssl_counters.ssltottlsv12sessionsrate} />
                <SSLCard title="TLS1.3 Rate/s" secure_cipher={true}  metric_value={ssl_counters.ssltottlsv13sessionsrate}/>  
                {/if}       
            </div>

            
            <!-- SSL Profile Table-->
            <div class="flex mt-24 ">
            <h1 class="text-xl font-mono text-gray-400  p-2">SSL Profiles</h1>
            
                <button on:click={() => {modal_new_ssl_profile = true}} class="group ml-2  bg-dark-sub-purple hover:bg-purple-900 text-gray-200 p-2 font-bold py-1 px-4 m-1 rounded inline-flex items-center">
                    <svg class="group-hover:animate-ping fill-current w-6 h-6 mr-2"  xmlns="http://www.w3.org/2000/svg" fill=null viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"> <path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" /> </svg>
                    <span>New Profile</span>
                </button>

            </div>
            <div class="grid grid-cols-1 bg-dark-foreground rounded-md ">          
                   <SSLProfileTable ssl_profile_list={ssl_profile_list} refresh_feed={() => get_sslprofiles()} />            
            </div>
            <!--Server Table-->
            
            <h1 class="text-2xl font-mono text-gray-400 mt-24 p-2">Assign Profiles</h1>
            <div class="min-w-full bg-dark-foreground rounded-md">

             {#if ssl_profile_list}              <!--Load Virtual servers after the API call is done-->
            <SSLServersTable bind:server_list={server_list} bind:ssl_profile_list={ssl_profile_list} bind:ciphergroup_list={ciphergroup_list}/>
            {/if}
        </div>
        <button on:click={() => console.log(server_list)}>This is a button with text</button>

</main>



<!--Modals-->

<!--New SSL Profile Modal-->
<Modal title="Create new SSL Profile"  bind:open={modal_new_ssl_profile}>
    <p class="text-sm font-mono">Entries have been prepopulated with best practices :). As long as you are on the SSL Profiles page, any new profile will be populated based on your last submission</p>
    <div class="flex items-center justify-left">
        <h1 class="text-md p-2 font-bold">Name:</h1>
        <input bind:value={default_data.name} class="ml-5 bg-gray-200 rounded-md p-2 border-1 w-full placeholder-red-800 " placeholder="String Value ">
    </div>
    <div class="flex items-center justify-left">
        <h1 class="text-md p-2 font-bold">sslprofiletype:</h1>
        <input bind:value={default_data.sslprofiletype} class="ml-5 bg-gray-200 rounded-md p-2 border-1 w-full placeholder-red-800 " placeholder="String Value (FrontEnd or BackEnd)">
    </div>
    <div class="flex items-center justify-left">
        <h1 class="text-md p-2 font-bold">ssllogprofile:</h1>
        <input bind:value={default_data.ssllogprofile} class="ml-5 bg-gray-200 rounded-md p-2 border-1 w-full placeholder-red-800" placeholder="String Value (Leave empty if none)">
    </div>
    <div class="flex items-center justify-left">
        <h1 class="text-md p-2 font-bold">dhcount:</h1>
        <input bind:value={default_data.dhcount} class="ml-5 bg-gray-200 rounded-md p-2 border-1 w-full placeholder-red-800" placeholder="String Value (Leave empty if none)">
    </div>
    <div class="flex items-center justify-left">
        <h1 class="text-md p-2 font-bold">dh:</h1>
        <input bind:value={default_data.dh} class="ml-5 bg-gray-200 rounded-md p-2 border-1 w-full placeholder-red-800" placeholder="String Value">
    </div>
    <div class="flex items-center justify-left">
        <h1 class="text-md p-2 font-bold">dhfile:</h1>
        <input bind:value={default_data.dhfile} class="ml-5 bg-gray-200 rounded-md p-2 border-1 w-full placeholder-red-800" placeholder="String Value (Leave empty if none)">
    </div>
    <div class="flex items-center justify-left">
        <h1 class="text-md p-2 font-bold">ersa:</h1>
        <input bind:value={default_data.ersa} class="ml-5 bg-gray-200 rounded-md p-2 border-1 w-full placeholder-red-800" placeholder="String Value">
    </div>
    <div class="flex items-center justify-left">
        <h1 class="text-md p-2 font-bold">ersacount:</h1>
        <input bind:value={default_data.ersacount} class="ml-5 bg-gray-200 rounded-md p-2 border-1 w-full placeholder-red-800" placeholder="String Value">
    </div>
    <div class="flex items-center justify-left">
        <h1 class="text-md p-2 font-bold">sessreuse:</h1>
        <input bind:value={default_data.sessreuse} class="ml-5 bg-gray-200 rounded-md p-2 border-1 w-full placeholder-red-800" placeholder="String Value">
    </div>
    <div class="flex items-center justify-left">
        <h1 class="text-md p-2 font-bold">sesstimeout:</h1>
        <input bind:value={default_data.sesstimeout} class="ml-5 bg-gray-200 rounded-md p-2 border-1 w-full placeholder-red-800" placeholder="String Value">
    </div>
    <div class="flex items-center justify-left">
        <h1 class="text-md p-2 font-bold">cipherredirect:</h1>
        <input bind:value={default_data.cipherredirect} class="ml-5 bg-gray-200 rounded-md p-2 border-1 w-full placeholder-red-800" placeholder="String Value">
    </div>
    <div class="flex items-center justify-left">
        <h1 class="text-md p-2 font-bold">cipherurl:</h1>
        <input bind:value={default_data.cipherurl} class="ml-5 bg-gray-200 rounded-md p-2 border-1 w-full placeholder-red-800" placeholder="String Value (Leave empty if none)">
    </div>
    <div class="flex items-center justify-left">
        <h1 class="text-md p-2 font-bold">clientauth:</h1>
        <input bind:value={default_data.clientauth} class="ml-5 bg-gray-200 rounded-md p-2 border-1 w-full placeholder-red-800" placeholder="String Value">
    </div>
    <div class="flex items-center justify-left">
        <h1 class="text-md p-2 font-bold">clientcert:</h1>
        <input bind:value={default_data.clientcert} class="ml-5 bg-gray-200 rounded-md p-2 border-1 w-full placeholder-red-800" placeholder="String Value (Leave empty if none)">
    </div>
    <div class="flex items-center justify-left">
        <h1 class="text-md p-2 font-bold">dhkeyexpsizelimit:</h1>
        <input bind:value={default_data.dhkeyexpsizelimit} class="ml-5 bg-gray-200 rounded-md p-2 border-1 w-full placeholder-red-800" placeholder="String Value">
    </div>
    <div class="flex items-center justify-left">
        <h1 class="text-md p-2 font-bold">sslredirect:</h1>
        <input bind:value={default_data.sslredirect} class="ml-5 bg-gray-200 rounded-md p-2 border-1 w-full placeholder-red-800" placeholder="String Value">
    </div>
    <div class="flex items-center justify-left">
        <h1 class="text-md p-2 font-bold">redirectportrewrite:</h1>
        <input bind:value={default_data.redirectportrewrite} class="ml-5 bg-gray-200 rounded-md p-2 border-1 w-full placeholder-red-800" placeholder="String Value">
    </div>
    <div class="flex items-center justify-left">
        <h1 class="text-md p-2 font-bold">ssl3:</h1>
        <input bind:value={default_data.ssl3} class="ml-5 bg-gray-200 rounded-md p-2 border-1 w-full placeholder-red-800" placeholder="String Value">
    </div>
    <div class="flex items-center justify-left">
        <h1 class="text-md p-2 font-bold">tls1:</h1>
        <input bind:value={default_data.tls1} class="ml-5 bg-gray-200 rounded-md p-2 border-1 w-full placeholder-red-800" placeholder="String Value">
    </div>
    <div class="flex items-center justify-left">
        <h1 class="text-md p-2 font-bold">tls11:</h1>
        <input bind:value={default_data.tls11} class="ml-5 bg-gray-200 rounded-md p-2 border-1 w-full placeholder-red-800" placeholder="String Value">
    </div>
    <div class="flex items-center justify-left">
        <h1 class="text-md p-2 font-bold">tls12:</h1>
        <input bind:value={default_data.tls12} class="ml-5 bg-gray-200 rounded-md p-2 border-1 w-full placeholder-red-800" placeholder="String Value">
    </div>
    <div class="flex items-center justify-left">
        <h1 class="text-md p-2 font-bold">tls13:</h1>
        <input bind:value={default_data.tls13} class="ml-5 bg-gray-200 rounded-md p-2 border-1 w-full placeholder-red-800" placeholder="String Value">
    </div>
    <div class="flex items-center justify-left">
        <h1 class="text-md p-2 font-bold">snienable:</h1>
        <input bind:value={default_data.snienable} class="ml-5 bg-gray-200 rounded-md p-2 border-1 w-full placeholder-red-800" placeholder="String Value">
    </div>
    <div class="flex items-center justify-left">
        <h1 class="text-md p-2 font-bold">ocspstapling:</h1>
        <input bind:value={default_data.ocspstapling} class="ml-5 bg-gray-200 rounded-md p-2 border-1 w-full placeholder-red-800" placeholder="String Value">
    </div>
    <div class="flex items-center justify-left">
        <h1 class="text-md p-2 font-bold">serverauth:</h1>
        <input bind:value={default_data.serverauth} class="ml-5 bg-gray-200 rounded-md p-2 border-1 w-full placeholder-red-800" placeholder="String Value">
    </div>
    <div class="flex items-center justify-left">
        <h1 class="text-md p-2 font-bold">commonname:</h1>
        <input bind:value={default_data.commonname} class="ml-5 bg-gray-200 rounded-md p-2 border-1 w-full placeholder-red-800" placeholder="String Value (Leave empty if none)">
    </div>
    <div class="flex items-center justify-left">
        <h1 class="text-md p-2 font-bold">pushenctrigger:</h1>
        <input bind:value={default_data.pushenctrigger} class="ml-5 bg-gray-200 rounded-md p-2 border-1 w-full placeholder-red-800" placeholder="String Value">
    </div>
    <div class="flex items-center justify-left">
        <h1 class="text-md p-2 font-bold">sendclosenotify:</h1>
        <input bind:value={default_data.sendclosenotify} class="ml-5 bg-gray-200 rounded-md p-2 border-1 w-full placeholder-red-800" placeholder="String Value">
    </div>
    <div class="flex items-center justify-left">
        <h1 class="text-md p-2 font-bold">cleartextport:</h1>
        <input bind:value={default_data.cleartextport} class="ml-5 bg-gray-200 rounded-md p-2 border-1 w-full placeholder-red-800" placeholder="String Value">
    </div>
    <div class="flex items-center justify-left">
        <h1 class="text-md p-2 font-bold">insertionencoding:</h1>
        <input bind:value={default_data.insertionencoding} class="ml-5 bg-gray-200 rounded-md p-2 border-1 w-full placeholder-red-800" placeholder="String Value">
    </div>
    <div class="flex items-center justify-left">
        <h1 class="text-md p-2 font-bold">denysslreneg:</h1>
        <input bind:value={default_data.denysslreneg} class="ml-5 bg-gray-200 rounded-md p-2 border-1 w-full placeholder-red-800" placeholder="String Value">
    </div>
    <div class="flex items-center justify-left">
        <h1 class="text-md p-2 font-bold">quantumsize:</h1>
        <input bind:value={default_data.quantumsize} class="ml-5 bg-gray-200 rounded-md p-2 border-1 w-full placeholder-red-800" placeholder="String Value">
    </div>
    <div class="flex items-center justify-left">
        <h1 class="text-md p-2 font-bold">strictcachecks:</h1>
        <input bind:value={default_data.strictcachecks} class="ml-5 bg-gray-200 rounded-md p-2 border-1 w-full placeholder-red-800" placeholder="String Value">
    </div>
    <div class="flex items-center justify-left">
        <h1 class="text-md p-2 font-bold">encrypttriggerpktcount:</h1>
        <input bind:value={default_data.encrypttriggerpktcount} class="ml-5 bg-gray-200 rounded-md p-2 border-1 w-full placeholder-red-800" placeholder="String Value">
    </div>
    <div class="flex items-center justify-left">
        <h1 class="text-md p-2 font-bold">pushflag:</h1>
        <input bind:value={default_data.pushflag} class="ml-5 bg-gray-200 rounded-md p-2 border-1 w-full placeholder-red-800" placeholder="String Value">
    </div>
    <div class="flex items-center justify-left">
        <h1 class="text-md p-2 font-bold">dropreqwithnohostheader:</h1>
        <input bind:value={default_data.dropreqwithnohostheader} class="ml-5 bg-gray-200 rounded-md p-2 border-1 w-full placeholder-red-800" placeholder="String Value">
    </div>
    <div class="flex items-center justify-left">
        <h1 class="text-md p-2 font-bold">snihttphostmatch:</h1>
        <input bind:value={default_data.snihttphostmatch} class="ml-5 bg-gray-200 rounded-md p-2 border-1 w-full placeholder-red-800" placeholder="String Value">
    </div>
    <div class="flex items-center justify-left">
        <h1 class="text-md p-2 font-bold">pushenctriggertimeout:</h1>
        <input bind:value={default_data.pushenctriggertimeout} class="ml-5 bg-gray-200 rounded-md p-2 border-1 w-full placeholder-red-800" placeholder="String Value">
    </div>
    <div class="flex items-center justify-left">
        <h1 class="text-md p-2 font-bold">ssltriggertimeout:</h1>
        <input bind:value={default_data.ssltriggertimeout} class="ml-5 bg-gray-200 rounded-md p-2 border-1 w-full placeholder-red-800" placeholder="String Value">
    </div>
    <div class="flex items-center justify-left">
        <h1 class="text-md p-2 font-bold">clientauthuseboundcachain:</h1>
        <input bind:value={default_data.clientauthuseboundcachain} class="ml-5 bg-gray-200 rounded-md p-2 border-1 w-full placeholder-red-800" placeholder="String Value">
    </div>
    <div class="flex items-center justify-left">
        <h1 class="text-md p-2 font-bold">sslinterception:</h1>
        <input bind:value={default_data.sslinterception} class="ml-5 bg-gray-200 rounded-md p-2 border-1 w-full placeholder-red-800" placeholder="String Value">
    </div>
    <div class="flex items-center justify-left">
        <h1 class="text-md p-2 font-bold">sslireneg:</h1>
        <input bind:value={default_data.sslireneg} class="ml-5 bg-gray-200 rounded-md p-2 border-1 w-full placeholder-red-800" placeholder="String Value">
    </div>
    <div class="flex items-center justify-left">
        <h1 class="text-md p-2 font-bold">ssliocspcheck:</h1>
        <input bind:value={default_data.ssliocspcheck} class="ml-5 bg-gray-200 rounded-md p-2 border-1 w-full placeholder-red-800" placeholder="String Value">
    </div>
    <div class="flex items-center justify-left">
        <h1 class="text-md p-2 font-bold">sslimaxsessperserver:</h1>
        <input bind:value={default_data.sslimaxsessperserver} class="ml-5 bg-gray-200 rounded-md p-2 border-1 w-full placeholder-red-800" placeholder="String Value">
    </div>
    <div class="flex items-center justify-left">
        <h1 class="text-md p-2 font-bold">sessionticket:</h1>
        <input bind:value={default_data.sessionticket} class="ml-5 bg-gray-200 rounded-md p-2 border-1 w-full placeholder-red-800" placeholder="String Value">
    </div>
    <div class="flex items-center justify-left">
        <h1 class="text-md p-2 font-bold">sessionticketlifetime:</h1>
        <input bind:value={default_data.sessionticketlifetime} class="ml-5 bg-gray-200 rounded-md p-2 border-1 w-full placeholder-red-800" placeholder="String Value">
    </div>
    <div class="flex items-center justify-left">
        <h1 class="text-md p-2 font-bold">sessionticketkeyrefresh:</h1>
        <input bind:value={default_data.sessionticketkeyrefresh} class="ml-5 bg-gray-200 rounded-md p-2 border-1 w-full placeholder-red-800" placeholder="String Value (Leave empty if none)">
    </div>
    <div class="flex items-center justify-left">
        <h1 class="text-md p-2 font-bold">sessionticketkeydata:</h1>
        <input bind:value={default_data.sessionticketkeydata} class="ml-5 bg-gray-200 rounded-md p-2 border-1 w-full placeholder-red-800" placeholder="String Value (Leave empty if none)">
    </div>
    <div class="flex items-center justify-left">
        <h1 class="text-md p-2 font-bold">sessionkeylifetime:</h1>
        <input bind:value={default_data.sessionkeylifetime} class="ml-5 bg-gray-200 rounded-md p-2 border-1 w-full placeholder-red-800" placeholder="String Value">
    </div>
    <div class="flex items-center justify-left">
        <h1 class="text-md p-2 font-bold">prevsessionkeylifetime:</h1>
        <input bind:value={default_data.prevsessionkeylifetime} class="ml-5 bg-gray-200 rounded-md p-2 border-1 w-full placeholder-red-800" placeholder="String Value">
    </div>
    <div class="flex items-center justify-left">
        <h1 class="text-md p-2 font-bold">hsts:</h1>
        <input bind:value={default_data.hsts} class="ml-5 bg-gray-200 rounded-md p-2 border-1 w-full placeholder-red-800" placeholder="String Value">
    </div>
    <div class="flex items-center justify-left">
        <h1 class="text-md p-2 font-bold">maxage:</h1>
        <input bind:value={default_data.maxage} class="ml-5 bg-gray-200 rounded-md p-2 border-1 w-full placeholder-red-800" placeholder="String Value">
    </div>
    <div class="flex items-center justify-left">
        <h1 class="text-md p-2 font-bold">includesubdomains:</h1>
        <input bind:value={default_data.includesubdomains} class="ml-5 bg-gray-200 rounded-md p-2 border-1 w-full placeholder-red-800" placeholder="String Value">
    </div>
    <div class="flex items-center justify-left">
        <h1 class="text-md p-2 font-bold">preload:</h1>
        <input bind:value={default_data.preload} class="ml-5 bg-gray-200 rounded-md p-2 border-1 w-full placeholder-red-800" placeholder="String Value">
    </div>
    <div class="flex items-center justify-left">
        <h1 class="text-md p-2 font-bold">skipclientcertpolicycheck:</h1>
        <input bind:value={default_data.skipclientcertpolicycheck} class="ml-5 bg-gray-200 rounded-md p-2 border-1 w-full placeholder-red-800" placeholder="String Value">
    </div>
    <div class="flex items-center justify-left">
        <h1 class="text-md p-2 font-bold">zerorttearlydata:</h1>
        <input bind:value={default_data.zerorttearlydata} class="ml-5 bg-gray-200 rounded-md p-2 border-1 w-full placeholder-red-800" placeholder="String Value">
    </div>
    <div class="flex items-center justify-left">
        <h1 class="text-md p-2 font-bold">tls13sessionticketsperauthcontext:</h1>
        <input bind:value={default_data.tls13sessionticketsperauthcontext} class="ml-5 bg-gray-200 rounded-md p-2 border-1 w-full placeholder-red-800" placeholder="String Value">
    </div>
    <div class="flex items-center justify-left">
        <h1 class="text-md p-2 font-bold">dhekeyexchangewithpsk:</h1>
        <input bind:value={default_data.dhekeyexchangewithpsk} class="ml-5 bg-gray-200 rounded-md p-2 border-1 w-full placeholder-red-800" placeholder="String Value">
    </div>
    <div class="flex items-center justify-left">
        <h1 class="text-md p-2 font-bold">allowextendedmastersecret:</h1>
        <input bind:value={default_data.allowextendedmastersecret} class="ml-5 bg-gray-200 rounded-md p-2 border-1 w-full placeholder-red-800" placeholder="String Value">
    </div>
    <div class="flex items-center justify-left">
        <h1 class="text-md p-2 font-bold">alpnprotocol:</h1>
        <input bind:value={default_data.alpnprotocol} class="ml-5 bg-gray-200 rounded-md p-2 border-1 w-full placeholder-red-800" placeholder="String Value (Leave empty if none)">
    </div>

  
  <svelte:fragment slot='footer'>
    <Button on:click={create_ssl_profile}>Create Profile</Button>
  </svelte:fragment>
</Modal>