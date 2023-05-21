<!--Populates the SSL Profile list table-->
<script>

import { getClient} from '@tauri-apps/api/http';
//Retrieve cookie data to use entered variables through session
const auth = ('; '+document.cookie).split(`; session_id=`).pop().split(';')[0];
const netscaler_ip = ('; '+document.cookie).split(`; netscaler_ip=`).pop().split(';')[0];
const protocol = ('; '+document.cookie).split(`; protocol=`).pop().split(';')[0];

// List that contains all the themes files found
export let themes_list = [];
let excluded_themes = ["Default", "Greenbubble", "X1"];





async function download_theme(themename){   
    const client = await getClient();

    // Convert the filepath for themes to a URI safe string
    let escapedLocation = encodeURIComponent(`/var/netscaler/logon/themes/${themename}`)

    // Get request to retrieve the partitions
    const response = await client.get(`${protocol}://${netscaler_ip}/nitro/v1/config/systemfile?args=filelocation:${escapedLocation}`, {headers:{'Content-Type' : 'application/json', 'Cookie' : `NITRO_AUTH_TOKEN=${auth}`}} )

    if(response.ok){
    // For each file in the response, download it into a folder
    response.data.systemfile.forEach(file => {
        if(file.filemode != "Directory"){
        
        // Download the file
        let element = document.createElement('a');
        element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(atob(file.filecontent)));
        //download to a new folder called themes
        element.setAttribute('download', `themes/${file.filename}`);
        element.style.display = 'none';
        document.body.appendChild(element);
        element.click();
        document.body.removeChild(element);
        }
    });
    
    
  }else{
    // Inform user of failure code
    alert("Something went wrong :(\n" + "Error:  \n" + response.data.message)
    console.log(response)
  }
}


</script>
    <!--Table-->
    <!-- button to download all partitions-->
    <div class="flex mt-24">   
        <div class="justify-start">
            <h1 class="text-xl font-mono text-gray-400 p-2">Custom Themes</h1>
        </div>
        <div class="justify-end">
            <button on:click={() => console.log("click")} class="group ml-2 bg-dark-sub-purple hover:bg-purple-900 text-gray-300 p-2 font-bold py-1 px-4 m-1 rounded inline-flex items-center">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m.75 12l3 3m0 0l3-3m-3 3v-6m-1.5-9H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z" />
                </svg>
                <span class="pl-2">Download All</span>
            </button>
        </div>
    </div>

    <table class=" text-md lg:text-md text-center text-gray-500 dark:text-gray-400 w-full">

        <thead class="text-md lg:text-lg text-dark-sub-purple uppercase border-2 border-dark-foreground font-mono bg-dark-background">
                <th scope="col" class="py-1.5 px-3 lg:py-3 lg:px-6">
                    <h1>Theme Name</h1>
                </th>
                <th scope="col" class="py-1.5 px-3 lg:py-3 lg:px-6">
                   
                </th>         
        </thead>

        <tbody>
            {#each themes_list as theme}
            <!--Only show if the name is theme.filename is not equal to any names in the name_list-->
            {#if !excluded_themes.includes(theme.filename)}
            
            <tr class="group bg-dark-foreground border-b border-b-gray-600 hover:bg-dark-background">
                <th scope="row" class="py-2 px-3 lg:py-4 lg:px-6  text-gray-400 font-bold truncate">
                    {theme.filename}
                </th>
                <th>
                    <button on:click={() => download_theme(theme.filename)} class="group ml-2  bg-dark-sub-purple hover:bg-purple-900 text-gray-300 p-2 font-bold py-1 px-4 m-1 rounded inline-flex items-center">
                        Download
                    </button>
                </th>
                
            </tr>
                {/if}
            {/each}            

        </tbody>
    </table>


