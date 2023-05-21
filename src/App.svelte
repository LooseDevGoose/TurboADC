<script>
  import { Router, Route} from "svelte-routing";


  //Pages

  //Login Screen
  import LoginScreen from "./Pages/LoginScreen.svelte";
  //Dashbaord
  import Dashboard from "./Pages/Dashboard.svelte";
  //SSL_Profiles
  import SSL_Profiles from "./Pages/SSLProfiles.svelte";
  //Advanced Backup
  import AdvancedBackup from "./Pages/AdvancedBackup.svelte";
  


  export let url = "";
</script>

<Router url="{url}">

  <div>
    <Route path="Dashboard" component={Dashboard}/>
    <Route path="SSLProfiles" component={SSL_Profiles}/>
    <Route path="AdvancedBackup" component={AdvancedBackup}/>
    <Route path="/"><LoginScreen/></Route>
  </div>
</Router>