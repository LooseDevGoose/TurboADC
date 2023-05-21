<script>
//These are the rows for the 'SSLServersTable'
//See SSLServersTable for more detailed information

import { getClient, Body} from '@tauri-apps/api/http';
import { Select } from 'flowbite-svelte';
import { onMount } from 'svelte';


export let server_list;
export let ssl_profile_list;
export let ciphergroup_list;
export let server;

//Cookie data
const auth = ('; '+document.cookie).split(`; session_id=`).pop().split(';')[0];
const netscaler_ip = ('; '+document.cookie).split(`; netscaler_ip=`).pop().split(';')[0];
const protocol = ('; '+document.cookie).split(`; protocol=`).pop().split(';')[0];

// Select options for the SSL Profile select box
let select_ssl_list;
select_ssl_list = ssl_profile_list.map(e => ({name: e.name, value: e.name}))
// Currently selected SSLProfile
let selected_ssl_profile;

// Select options for the Cipher suit select box
let select_cipher_list;
select_cipher_list = ciphergroup_list.map(e => ({name: e.ciphergroupname, value: e.ciphergroupname}));
// Currently selected Ciphergroup
let selected_cipher_group;

// Funtion to apply (set) selected SSL profile
async function set_ssl_profile(){   
    
    let default_data = {
        vservername: server.vservername,
        sslprofile: selected_ssl_profile
        }

    if(default_data.vservername != "None Applied"){

        const client = await getClient();
        const data =  Body.json({

            sslvserver: default_data
        })

        // POST request to login endpoint on NetScaler
        const response = await client.put(`${protocol}://${netscaler_ip}/nitro/v1/config/sslvserver`, data, {headers:{'Content-Type' : 'application/json', 'Cookie' : `NITRO_AUTH_TOKEN=${auth}`}} )

        if(response.ok){

            // Assign data to variable for HTML useage
            let response_data = await response.data
            console.log(response_data)
            alert("Profile(s) Updated!")
            //refresh feed
            get_sslprofiles()
        }else{
            alert("Something went wrong :(\n" + "Error:  \n" + response.data.message)
        }
    }
}

</script>

<tr class="group bg-dark-foreground border-b border-b-gray-600 hover:bg-dark-background">
    <th scope="row" class="py-4 px-6  text-gray-400 font-bold whitespace-nowrap dark:text-white">
        {server.vservername}
    </th>
    <!--SSL Profile Selection-->
    <td class="py-4 px-6 font-bold text-gray-400">
        {#if server.sslprofile}
            <Select items={select_ssl_list} bind:value={selected_ssl_profile} placeholder={server.sslprofile}/>
           
        {:else}
            <Select items={select_ssl_list} bind:value={selected_ssl_profile} placeholder="None applied"/>
        {/if}
    </td>
    <!--CipherSuite Selection-->
     <td class="py-4 px-6 font-bold text-gray-400">
        {#if server.ciphergroupname}
            {console.log(server)}
            <Select items={select_cipher_list} bind:value={selected_cipher_group} placeholder={server.ciphergroupname}/>
        {:else}
            <Select items={select_cipher_list} bind:value={selected_cipher_group} placeholder="None applied"/>
        {/if}
    </td>
    <td class="py-4 px-6 font-bold text-gray-400">
            <div class="flex items-center">
                <button on:click={() => set_ssl_profile()} class=" bg-dark-sub-purple hover:bg-purple-800 p-2 m-1 rounded-md font-mono text-gray-200 ">Apply</button>
                </div>
    </td>
</tr>

