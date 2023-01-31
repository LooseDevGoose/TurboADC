<!--Populates the SSL Profile list table-->
<script>

import { getClient, Body} from '@tauri-apps/api/http';
import { Button, Modal} from 'flowbite-svelte';
export let ssl_profile_list = [];
export let refresh_feed;

//Cookie data
const auth = ('; '+document.cookie).split(`; session_id=`).pop().split(';')[0];
const netscaler_ip = ('; '+document.cookie).split(`; netscaler_ip=`).pop().split(';')[0];
const protocol = ('; '+document.cookie).split(`; protocol=`).pop().split(';')[0];



//Modal to edit SSL profile
let modal_edit_ssl_profile = false;

//SSL Profile data format, this can only contain the name + editable fields. Otherwise the API 'put' will fail.
let ssl_profile_data = {

      name: "Turbo_Netscaler_SSLProfile",
      ssl3 : "ENABLED",
      tls1 : "DISABLED",
      tls11 : "DISABLED",
      tls12 : "ENABLED",
      tls13 : "DISABLED",
      hsts : "ENABLED"

}

function modal_func(profile){

    ssl_profile_data.name = profile.name
    ssl_profile_data.ssl3 = profile.ssl3
    ssl_profile_data.tls1 = profile.tls1
    ssl_profile_data.tls11 = profile.tls11
    ssl_profile_data.tls12 = profile.tls12
    ssl_profile_data.tls13 = profile.tls13
    ssl_profile_data.hsts = profile.hsts
    
    console.log(profile)
    modal_edit_ssl_profile = true
}

//Edit SSL profile
async function edit_ssl_profile(){   

    //This ugly bit of codes converts all the number values (stupid json) that are strings, to actual numbers.
    for (let key in ssl_profile_data) {
        if (typeof ssl_profile_data[key] === 'object') {
            convertStringsToNumbers(ssl_profile_data[key]);
        } else if (!isNaN(ssl_profile_data[key])) {
            ssl_profile_data[key] = Number(ssl_profile_data[key]);
        }
    }



    const client = await getClient();

    const data =  Body.json({

        sslprofile: ssl_profile_data
    })
    console.log(data)
    //Put request to change SSL Profile data
    const response = await client.put(`${protocol}://${netscaler_ip}/nitro/v1/config/sslprofile`, data, {headers:{'Content-Type' : 'application/json', 'Cookie' : `NITRO_AUTH_TOKEN=${auth}`}} )

    if(response.ok){
    //Inform user
    alert("Profile Edited!")
    //Close the modal
    modal_edit_ssl_profile = false
    refresh_feed();
  }else{
    //Inform user of failure code
    alert("Something went wrong :(\n" + "Error:  \n" + response.data.message)
  }
    console.log(response)



}

</script>




    

    <table class=" text-xs lg:text-md text-center text-gray-500 dark:text-gray-400">
        <thead class="text-xs lg:text-lg text-dark-sub-purple uppercase border-2 border-dark-foreground font-mono bg-dark-background">
        
                <th scope="col" class="py-1.5 px-3 lg:py-3 lg:px-6">
                 
                </th>
                <th scope="col" class="py-1.5 px-3 lg:py-3 lg:px-6">
                    <h1>profile name</h1>
                </th>
                <th scope="col" class="py-1.5 px-3 lg:py-3 lg:px-6">
                    SSLv3
                </th>
                  <th scope="col" class="py-1.5 px-3 lg:py-3 lg:px-6">
                    TLS1.0
                </th>
                  <th scope="col" class="py-1.5 px-3 lg:py-3 lg:px-6">
                    TLS1.1
                </th>
                  <th scope="col" class="py-1.5 px-3 lg:py-3 lg:px-6">
                    TLS1.2
                </th>
                  <th scope="col" class="py-1.5 px-3 lg:py-3 lg:px-6">
                    TLS1.3
                </th>
                  <th scope="col" class="py-1.5 px-3 lg:py-3 lg:px-6">
                    HSTS
                </th>
            
        </thead>
        <tbody>
        {#each Object.values(ssl_profile_list) as profile}
            <tr class="group bg-dark-foreground border-b border-b-gray-600 hover:bg-dark-background">
                <td class="p-2 lg:p-4">
                    <div class="flex items-center">
                         <button on:click={() => modal_func(profile)} class=" bg-dark-sub-purple hover:bg-purple-800 p-2 m-1 rounded-md font-mono text-gray-200 ">Edit</button>
                         </div>
                </td>
                <th scope="row" class="py-2 px-3 lg:py-4 lg:px-6  text-gray-400 font-bold truncate">
                    {profile.name}
                </th>
                {#if profile.ssl3 == 'DISABLED'}
                <td class="py-2 px-3 lg:py-4 lg:px-6 font-bold text-gray-400">
                    {profile.ssl3} 
                </td>
                {:else}
                 <td class="py-2 px-3 lg:py-4 lg:px-6 font-bold text-red-800">
                    {profile.ssl3} 
                </td>
                {/if}

                {#if profile.tls1 == 'DISABLED'}
                <td class="py-2 px-3 lg:py-4 lg:px-6 font-bold text-gray-400">
                    {profile.tls1} 
                </td>
                {:else}
                 <td class="py-2 px-3 lg:py-4 lg:px-6 font-bold text-red-800">
                    {profile.tls1} 
                </td>
                {/if}
                {#if profile.tls11 == 'DISABLED'}
                <td class="py-2 px-3 lg:py-4 lg:px-6 font-bold text-gray-400">
                    {profile.tls11} 
                </td>
                {:else}
                 <td class="py-2 px-3 lg:py-4 lg:px-6 font-bold text-red-800">
                    {profile.tls11} 
                </td>
                {/if}
                                
                {#if profile.tls12 == 'ENABLED'}
                <td class="py-2 px-3 lg:py-4 lg:px-6 font-bold text-gray-400">
                    {profile.tls12} 
                </td>
                {:else}
                 <td class="py-2 px-3 lg:py-4 lg:px-6 font-bold text-red-800">
                    {profile.tls12} 
                </td>
                {/if}

                     {#if profile.tls13 == 'ENABLED'}
                <td class="py-2 px-3 lg:py-4 lg:px-6 font-bold text-gray-400">
                    {profile.tls13} 
                </td>
                {:else}
                 <td class="py-2 px-3 lg:py-4 lg:px-6 font-bold text-red-800">
                    {profile.tls13} 
                </td>
                {/if}

                {#if profile.hsts == 'ENABLED'}
                <td class="py-2 px-3 lg:py-4 lg:px-6 font-bold text-gray-400">
                    {profile.hsts} 
                </td>
                {:else}
                 <td class="py-2 px-3 lg:py-4 lg:px-6 font-bold text-red-800">
                    {profile.hsts} 
                </td>
                {/if}


            </tr>
             {/each}

        </tbody>
    </table>

  




<!--Edit SSL Profile Modal-->
<Modal title="Edit SSL Profile"  bind:open={modal_edit_ssl_profile}>
     <div class="flex items-center justify-left">
        <h1 class="text-md p-2 font-bold">ssl3:</h1>
        <input bind:value={ssl_profile_data.ssl3} class="ml-5 bg-gray-200 rounded-md p-2 border-1 w-full placeholder-red-800" placeholder="String Value">
    </div>
    <div class="flex items-center justify-left">
        <h1 class="text-md p-2 font-bold">tls1:</h1>
        <input bind:value={ssl_profile_data.tls1} class="ml-5 bg-gray-200 rounded-md p-2 border-1 w-full placeholder-red-800" placeholder="String Value">
    </div>
    <div class="flex items-center justify-left">
        <h1 class="text-md p-2 font-bold">tls11:</h1>
        <input bind:value={ssl_profile_data.tls11} class="ml-5 bg-gray-200 rounded-md p-2 border-1 w-full placeholder-red-800" placeholder="String Value">
    </div>
    <div class="flex items-center justify-left">
        <h1 class="text-md p-2 font-bold">tls12:</h1>
        <input bind:value={ssl_profile_data.tls12} class="ml-5 bg-gray-200 rounded-md p-2 border-1 w-full placeholder-red-800" placeholder="String Value">
    </div>
    <div class="flex items-center justify-left">
        <h1 class="text-md p-2 font-bold">tls13:</h1>
        <input bind:value={ssl_profile_data.tls13} class="ml-5 bg-gray-200 rounded-md p-2 border-1 w-full placeholder-red-800" placeholder="String Value">
    </div>
        <div class="flex items-center justify-left">
        <h1 class="text-md p-2 font-bold">HSTS:</h1>
        <input bind:value={ssl_profile_data.hsts} class="ml-5 bg-gray-200 rounded-md p-2 border-1 w-full placeholder-red-800" placeholder="String Value">
    </div>
   

  
  <svelte:fragment slot='footer'>
    <Button on:click={() => (edit_ssl_profile())}>Save Profile Changes</Button>
  </svelte:fragment>
</Modal>