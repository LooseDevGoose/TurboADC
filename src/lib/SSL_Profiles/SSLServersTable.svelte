<script>
//This table creates a row for each SSLVirtualServer
//Each row has a select box, that is defaulted to the currently applied profile
//Changing the select box does not do anything on the NetScaler untill the 'Apply' button is pressed. 


import SSLServersTable_row from './SSLServersTable_row.svelte';

//Complete SSL server list & Complete SSL Profile list
export let server_list;
export let ssl_profile_list;

//Index to keep track of which entry belongs to which server
let server;




</script>    

<table class="w-full text-sm text-left text-gray-500 dark:text-gray-400">
    <thead class="text-lg text-dark-sub-purple uppercase border-2 border-dark-foreground font-mono bg-dark-background">
        <th scope="col" class="py-3 px-6">
            Virtual Server
        </th>
        <th scope="col" class="py-3 px-6">
            SSL Profile
        </th>
        <th scope="col" class="py-3 px-6">
        </th> 
    </thead>
    <tbody>
        {#key server_list.length > 0 }
            {#each server_list as server}
                <SSLServersTable_row bind:server_list={server_list} bind:ssl_profile_list={ssl_profile_list} server={server}/>
            {/each}
        {/key}
    </tbody>
</table>