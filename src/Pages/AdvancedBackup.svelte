<script>
import { getClient} from '@tauri-apps/api/http';
import { onMount } from 'svelte';
import { Button, Modal} from 'flowbite-svelte';

import PageTitleCard from '../lib/General/PageTitleCard.svelte';
import NavBar from '../lib/General/NavBar.svelte';

import Download_Icon from '../../public/Icons/Download_Icon.svg';
import PartitionsTable from '../lib/Advanced Backup/PartitionsTable.svelte';
import LicensesTable from '../lib/Advanced Backup/LicensesTable.svelte';
import ThemesTable from '../lib/Advanced Backup/ThemesTable.svelte';
 


// List that contains all the partitions
let partitions_list;
// List that contains all the license files
let licenses_list;
// List that contains all the themes
let themes_list;
// Contains the file content for readmode, retrieved from child component
let file_object = {filename: "", filecontent: ""};
// Modal Size
let modal_size = "sm";
// Modal open/close control
let readmode_modal_open = false;

//Retrieve cookie data to use entered variables through session
const auth = ('; '+document.cookie).split(`; session_id=`).pop().split(';')[0];
const netscaler_ip = ('; '+document.cookie).split(`; netscaler_ip=`).pop().split(';')[0];
const protocol = ('; '+document.cookie).split(`; protocol=`).pop().split(';')[0];


async function get_partitions(){   
    const client = await getClient();
    // Get request to retrieve the partitions
    const response = await client.get(`${protocol}://${netscaler_ip}/nitro/v1/config/nspartition`, {headers:{'Content-Type' : 'application/json', 'Cookie' : `NITRO_AUTH_TOKEN=${auth}`}} )

    if(response.ok){
    // Populate the partitions list
      partitions_list = response.data.nspartition;
  }else{
    // Inform user of failure code
    alert("Something went wrong :(\n" + "Error:  \n" + response.data.message)
  }
    console.log(response)
}

async function get_licenses(){   
    const client = await getClient();

    // Convert the filepath for licenses to a URI safe string
    let escapedLocation = encodeURIComponent("/nsconfig/license/")

    // Get request to retrieve the partitions
    const response = await client.get(`${protocol}://${netscaler_ip}/nitro/v1/config/systemfile?args=filelocation:${escapedLocation}`, {headers:{'Content-Type' : 'application/json', 'Cookie' : `NITRO_AUTH_TOKEN=${auth}`}} )

    if(response.ok){
    // map thorugh response and add all files ending with .lic to the licenses list
    licenses_list = response.data.systemfile.filter(file => file.filename.endsWith(".lic")) 

  }else{
    // Inform user of failure code
    alert("Something went wrong :(\n" + "Error:  \n" + response.data.message)
  }
    console.log(response)
}

async function get_themes(){   
    const client = await getClient();

    // Convert the filepath for themes to a URI safe string
    let escapedLocation = encodeURIComponent("/var/netscaler/logon/themes/")

    // Get request to retrieve the partitions
    const response = await client.get(`${protocol}://${netscaler_ip}/nitro/v1/config/systemfile?args=filelocation:${escapedLocation}`, {headers:{'Content-Type' : 'application/json', 'Cookie' : `NITRO_AUTH_TOKEN=${auth}`}} )

  if(response.ok){
      //Add each entry in the responses response.data.systemfile to the themes_list
      themes_list = response.data.systemfile;
  }else{
    // Inform user of failure code
    alert("Something went wrong :(\n" + "Error:  \n" + response.data.message)
    console.log(response)
  }
}

//Upon first mount, get Metric Data
onMount(async () => prescript()) 

function prescript(){
    get_partitions();
    get_licenses();
    get_themes();
}

</script>

<main class="bg-[#222222] h-screen w-screen">
    <div class="flex">
    <NavBar/>       
        <!--Main container (|NAVBAR| |This container|)-->
        <div class="px-20 py-12 max-w-full max-h-full">      
            <!--Title Card-->
            <PageTitleCard title="Advanced Backup" icon={Download_Icon} />        
            <!--Import Backup Table-->
            <LicensesTable licenses_list={licenses_list} bind:file_object={file_object} bind:readmode_modal_open={readmode_modal_open}/>
            <PartitionsTable partitions_list={partitions_list} bind:file_object={file_object} bind:readmode_modal_open={readmode_modal_open}/>
            <ThemesTable themes_list={themes_list} />
            </div>
        </div>

</main>


<Modal title="Reading: {file_object.filename}" bind:open={readmode_modal_open} size="xl">
 <!-- Create each line on a new line-->
 <div class="whitespace-pre">
  {file_object.filecontent}
 </div>
 
</Modal>