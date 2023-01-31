<script>
  import { Router, Link, Route} from "svelte-routing";


  //Pages

  //Login Screen
  import LoginScreen from "./Pages/LoginScreen.svelte";
  //Dashbaord
  import Dashboard from "./Pages/Dashboard.svelte";
  //SSL_Profiles
  import SSL_Profiles from "./Pages/SSL_Profiles.svelte";
  


  export let url = "";
</script>

<Router url="{url}">

  <div>
    <Route path="Dashboard" component={Dashboard}/>
    <Route path="SSL_Profiles" component={SSL_Profiles}/>
    <Route path="/"><LoginScreen/></Route>
   <!--<Route path="blog" component="{Blog}" /> -->
  </div>
</Router>