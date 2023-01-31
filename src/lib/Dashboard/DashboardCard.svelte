<script>

export let title = "Undefined Title";
export let metric_value = "N/A";
export let second_value = "";
export let helper_icon;


</script>

<main class="mt-5">
    <div class="bg-dark-foreground  rounded-md hover:shadow-purple-800 shadow-lg">
        <div class="flex-row p-4">
            
            <!--Title Text-->
            <h1 class=" text-sm  lg:text-lg font-mono text-gray-400 whitespace-nowrap overflow-hidden">{title}</h1>
            
            <!--Metric Value + Icon-->
           
            {#if second_value == ""}
             <!--Create a signle line card-->
            <span class="flex text-gray-300 items-center over mt-2">
                {#if helper_icon != ""}
                <!--Only show icon field if applicable-->
                <img src={helper_icon} height="36" width="36" class="" alt="status_icon"/>
                {/if}
                <h1 class="text-md lg:text-lg font-bold text-lime-500 ml-4 overflow-hidden whitespace-nowrap appearance-none">{metric_value}</h1>
               
            </span>
            
            <!--Create a double lined card instead-->
            {:else}

            <span class="flex text-gray-300 items-center over mt-2">
            <img src={helper_icon} height="36" width="36" class="" alt="status_icon"/>
            <h1 class="text-xs lg:text-md font-bold text-lime-500 ml-4 overflow-hidden whitespace-nowrap truncate ">{metric_value}</h1>
            <h1 class="text-xs lg:text-md font-bold text-lime-500 ml-4 overflow-hidden whitespace-nowrap truncate">{second_value}</h1>
            </span>

            {/if}
        </div>
    </div>
</main>