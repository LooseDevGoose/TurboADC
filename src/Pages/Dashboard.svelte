<script>
import { getClient} from '@tauri-apps/api/http';
import { onMount } from 'svelte';

import PageTitleCard from '../lib/General/PageTitleCard.svelte';
import NavBar from '../lib/General/NavBar.svelte';
import DashboardCard from '../lib/Dashboard/DashboardCard.svelte';

import Dashboard_Icon from '../../public/Icons/Dashboard_Icon.svg';
import CPU_Icon from '../../public/Icons/CPU_Icon.svg';
import Throughput_Icon from '../../public/Icons/Throughput_Icon.svg';
import Disk_Icon from '../../public/Icons/Disk_Icon.svg';
import Memory_Icon from '../../public/Icons/Memory_Icon.svg';


let cpu_consumption;
let disk_consumption
let throughput_consumption_in;
let throughput_consumption_out;
let memory_consumption;

//Retrieve cookie data to use entered variables through session
const auth = ('; '+document.cookie).split(`; session_id=`).pop().split(';')[0];
const netscaler_ip = ('; '+document.cookie).split(`; netscaler_ip=`).pop().split(';')[0];
const protocol = ('; '+document.cookie).split(`; protocol=`).pop().split(';')[0];


//Upon first mount, get Metric Data
onMount(async () => get_ns_data()) 
    

//Get all Analytical Data from NS
async function get_ns_data(){

    const client = await getClient();
    const response = await client.get(`${protocol}://${netscaler_ip}/nitro/v1/stat/ns`, {headers:{'Content-Type' : 'application/json', 'Cookie' : `NITRO_AUTH_TOKEN=${auth}`}} )

    if(response.ok){

        //Set Metrics
        cpu_consumption=response.data.ns.cpuusage;
        disk_consumption=response.data.ns.disk1perusage;
        memory_consumption=Math.floor(response.data.ns.memusagepcnt);

        throughput_consumption_in= +(response.data.ns.totrxmbits * 0.000008);
        if(throughput_consumption_in <=1){
            throughput_consumption_in="< 1"
        }

        throughput_consumption_out= +(response.data.ns.tottxmbits * 0.000008);
        if(throughput_consumption_out <=1){
            throughput_consumption_out="< 1"
        }

      
    
    }
    }
    //Refetch the metrics every 15 seconds
    setInterval(get_ns_data, 15000);

</script>

<main class="bg-[#222222] h-screen w-screen">
    <div class="flex">
    <NavBar/>
        
        <!--Main container (right side)-->
        <div class="px-20 py-12 max-w-full max-h-full">
         
            <!--Title Card-->
            <PageTitleCard title="Dashboard" icon={Dashboard_Icon} />
            
            <!--First layer of cards -> 4 horizontal -->
            <div class="grid gap-4 justify-between grid grid-cols-4">
                <DashboardCard title="CPU Consumption" helper_icon={CPU_Icon} metric_value={cpu_consumption + "%"}/>
                <DashboardCard title="Disk Space" helper_icon={Disk_Icon} metric_value = {disk_consumption + "%"}/>
                <DashboardCard title="Throughput"metric_value={"I:" + throughput_consumption_in + " Mbps"}  second_value={"O:" + throughput_consumption_out + " Mbps"} helper_icon={Throughput_Icon} />
                <DashboardCard title="Memory Consumption" helper_icon={Memory_Icon} metric_value={memory_consumption + "%"}/>
            </div>

            <!--Events-->
            <h1 class="text-2xl font-mono text-gray-400  mt-24 p-2">Information</h1>
            <div class="w-full h-72 bg-dark-foreground rounded-md">
                 
            </div>

          
  
        </div>
    </div>

    

</main>

