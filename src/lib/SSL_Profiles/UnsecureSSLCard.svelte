<script>

export let title = "Undefined Title";
export let metric_value = 0;




</script>

<main class="mt-5">
    <div class="bg-dark-foreground rounded-md hover:shadow-purple-800 shadow-lg">
        <div class="flex-row p-2">

            <!--Title Text-->
            <h1 class=" text-xl font-mono text-gray-400 overflow-hidden">{title}</h1>

            {#if metric_value > 0}
            <h1 class="text-2xl font-bold text-red-800 overflow-hidden">{metric_value}</h1>
            {:else}
            <h1 class="text-2xl font-bold text-lime-600 overflow-hidden">{metric_value}</h1>
            {/if}
            
            <!--Create a double lined card instead-->
         
        </div>
    </div>
</main>