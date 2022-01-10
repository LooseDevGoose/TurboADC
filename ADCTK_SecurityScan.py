# Page for everything related to the security tab

# Import DataTable Libs
from kivy.metrics import dp
from deepdiff import DeepDiff
from pprint import pprint

# Import Netscaler Nitro libs for editing resources
from nssrc.com.citrix.netscaler.nitro.resource.config.lb.lbvserver import lbvserver
from nssrc.com.citrix.netscaler.nitro.resource.config.cs.csvserver import csvserver
from nssrc.com.citrix.netscaler.nitro.resource.config.vpn.vpnvserver import vpnvserver
from nssrc.com.citrix.netscaler.nitro.resource.config.gslb.gslbvserver import gslbvserver
from nssrc.com.citrix.netscaler.nitro.resource.config.authentication.authenticationvserver import authenticationvserver
from nssrc.com.citrix.netscaler.nitro.resource.config.ssl.sslvserver import sslvserver
from nssrc.com.citrix.netscaler.nitro.resource.config.ssl.sslprofile import sslprofile

# Import API Handling requirements
import requests
import time
import json

# Import RegEx handeling
import re

# Import Other Files
import ADCTK_UI


class Fill_Data_Table_With_Virtual_Servers():

    def ServerListData(self, ns_session):

        # Entry types for 'Generate Report' syntax
        nameentries = []
        ipentries = []
        typeentries = []

        # Fetches all the present LB_Virtual Servers
        result = lbvserver.get(ns_session)

        for i in (range(0, len(result))):
            nameentries.append(result[i].name)
            ipentries.append(result[i].ipv46)
            typeentries.append("Load Balancing Virtual Server")

        result = csvserver.get(ns_session)
        for i in (range(0, len(result))):
            nameentries.append(result[i].name)
            ipentries.append(result[i].ipv46)
            typeentries.append("Content Switching Virtual Server")

        result = vpnvserver.get(ns_session)
        for i in (range(0, len(result))):
            nameentries.append(result[i].name)
            ipentries.append(result[i].ipv46)
            typeentries.append("VPN Virtual Server")

        result = authenticationvserver.get(ns_session)
        for i in (range(0, len(result))):
            nameentries.append(result[i].name)
            ipentries.append(result[i].ipv46)
            typeentries.append("Authentication Virtual Server")

        result = gslbvserver.get(ns_session)
        for i in (range(0, len(result))):
            nameentries.append(result[i].name)
            ipentries.append(result[i].ipv46)
            typeentries.append("GSLB Virtual Server")

        return (nameentries, ipentries, typeentries)

    def Set_Column_Data(self):

        columndata = [
            ("No.", dp(20)),
            ("Name", dp(50)),
            ("Virtual IP", dp(30)),
            ("Type", dp(50)),
        ]

        return columndata

    def Set_Row_Data(self, ns_session):

        data = self.ServerListData(ns_session)
        rowdata = [(f"{i + 1}", data[0][i], data[1][i], data[2][i])
                   for i in (range(0, len(data[0])))]
        return rowdata


class SSL_Hardening_Procedure():

    def Check_If_SSL_Profile_Present(self, ServerName, ns_session, Selected_Template):

        try:
            # Instantiate Selected Template in class
            self.Selected_Template = Selected_Template
            # Declare SSL Server entry
            ssl_vserver_entry = sslvserver()
            # Define the name of the SSL Server to check
            ssl_vserver_entry.vservername = f"{ServerName}"
            # Set Current SSL Server to be able to retrieve current configs
            Current_SSL_Server = ssl_vserver_entry.get(ns_session, ServerName)

            # Check if a profile is present AND that it is created by Turbo_ADC
            # if true,  start evaluation against selected template
            if Current_SSL_Server.sslprofile == f"{ServerName}_Turbo_ADC_Profile":
                print("Profile exists")
                return self.Update_SSL_Profile_And_Get_Values(ns_session, ServerName)
            # If profile is not present or not made by Turbo_ADC create a new one
            else:
                return self.Create_New_SSL_Profile(ServerName, ns_session)

        except Exception as error:

            errormessage = (
                "Error Create_New_SSL_Profile1: " + str(error.args))
            print(errormessage)

    def Create_New_SSL_Profile(self, ServerName, ns_session):

        try:
            # Create new SSL Profile
            profile_creation = sslprofile()
            profile_creation.name = f"{ServerName}_Turbo_ADC_Profile"

            # Will fail if profile exists and continue assignment of the existing ADC_Turbo profile (prevents double entries)
            profile_creation.name = f"{ServerName}_Turbo_ADC_Profile"
            profile_creation.add(ns_session, profile_creation)

        except Exception as error:

            errormessage = (
                "Error Create_New_SSL_Profile2: " + str(error.args))
            print(errormessage)

        try:
            # Assign new SSL profile to server
            ssl_vserver_entry = sslvserver()
            ssl_vserver_entry.vservername = f"{ServerName}"
            ssl_vserver_entry.sslprofile = f"{ServerName}_Turbo_ADC_Profile"
            ssl_vserver_entry.update(ns_session, ssl_vserver_entry)
            return self.Update_SSL_Profile_And_Get_Values(ns_session, ServerName)

        except Exception as error:

            errormessage = (
                "Error Create_New_SSL_Profile3: " + str(error.args))
            print(errormessage)

    def Update_SSL_Profile_And_Get_Values(self, ns_session, ServerName):
        try:

            profile_entry = sslprofile()
            profile_entry.name = f"{ServerName}_Turbo_ADC_Profile"

            # Get SSL Profile settings
            get_value_of_setting = profile_entry.get(
                ns_session, profile_entry.name)
            # Assign current settings to dict
            current_ssl_profile_values = {
                "sslprofile": {
                    "allowextendedmastersecret": f"{get_value_of_setting.allowextendedmastersecret}",
                    "alpnprotocol": f"{get_value_of_setting.alpnprotocol}",
                    "dhekeyexchangewithpsk": f"{get_value_of_setting.dhekeyexchangewithpsk}",
                    "preload": f"{get_value_of_setting.preload}",
                    "snihttphostmatch": f"{get_value_of_setting.snihttphostmatch}",
                    "sslinterception": f"{get_value_of_setting.sslinterception}",
                    "ssllogprofile": f"{get_value_of_setting.ssllogprofile}",
                    "tls13": f"{get_value_of_setting.tls13}",
                    "tls13sessionticketsperauthcontext": f"{get_value_of_setting.tls13sessionticketsperauthcontext}",
                    "zerorttearlydata": f"{get_value_of_setting.zerorttearlydata}",
                    "dh": f"{get_value_of_setting.dh}",
                    "dhfile": f"{get_value_of_setting.dhfile}",
                    "dhcount": f"{get_value_of_setting.dhfile}",
                    "dhkeyexpsizelimit": f"{get_value_of_setting.dhkeyexpsizelimit}",
                    "ersa": f"{get_value_of_setting.ersa}",
                    "ersacount": f"{get_value_of_setting.ersacount}",
                    "sessreuse": f"{get_value_of_setting.sessreuse}",
                    "sesstimeout": f"{get_value_of_setting.sesstimeout}",
                    "cipherredirect": f"{get_value_of_setting.cipherredirect}",
                    "cipherurl": f"{get_value_of_setting.cipherurl}",
                    "clientauth": f"{get_value_of_setting.clientauth}",
                    "clientcert": f"{get_value_of_setting.clientcert}",
                    "sslredirect": f"{get_value_of_setting.sslredirect}",
                    "redirectportrewrite": f"{get_value_of_setting.redirectportrewrite}",
                    "ssl3": f"{get_value_of_setting.ssl3}",
                    "tls1": f"{get_value_of_setting.tls1}",
                    "tls11": f"{get_value_of_setting.tls11}",
                    "tls12": f"{get_value_of_setting.tls12}",
                    "snienable": f"{get_value_of_setting.snienable}",
                    "ocspstapling": f"{get_value_of_setting.ocspstapling}",
                    "serverauth": f"{get_value_of_setting.serverauth}",
                    "commonname": f"{get_value_of_setting.commonname}",
                    "pushenctrigger": f"{get_value_of_setting.pushenctrigger}",
                    "sendclosenotify": f"{get_value_of_setting.sendclosenotify}",
                    "cleartextport": f"{get_value_of_setting.cleartextport}",
                    "insertionencoding": f"{get_value_of_setting.insertionencoding}",
                    "denysslreneg": f"{get_value_of_setting.denysslreneg}",
                    "quantumsize": f"{get_value_of_setting.quantumsize}",
                    "strictcachecks": f"{get_value_of_setting.strictcachecks}",
                    "encrypttriggerpktcount": f"{get_value_of_setting.encrypttriggerpktcount}",
                    "pushflag": f"{get_value_of_setting.pushflag}",
                    "dropreqwithnohostheader": f"{get_value_of_setting.dropreqwithnohostheader}",
                    "pushenctriggertimeout": f"{get_value_of_setting.pushenctriggertimeout}",
                    "ssltriggertimeout": f"{get_value_of_setting.ssltriggertimeout}",
                    "sslprofiletype": f"{get_value_of_setting.sslprofiletype}",
                    "clientauthuseboundcachain": f"{get_value_of_setting.clientauthuseboundcachain}",
                    "sslireneg": f"{get_value_of_setting.sslireneg}",
                    "ssliocspcheck": f"{get_value_of_setting.ssliocspcheck}",
                    "sslimaxsessperserver": f"{get_value_of_setting.sslimaxsessperserver}",
                    "sessionticket": f"{get_value_of_setting.sessionticket}",
                    "sessionticketlifetime": f"{get_value_of_setting.sessionticketlifetime}",
                    "sessionticketkeyrefresh": f"{get_value_of_setting.sessionticketkeyrefresh}",
                    "sessionticketkeydata": f"{get_value_of_setting.sessionticketkeydata}",
                    "sessionkeylifetime": f"{get_value_of_setting.sessionkeylifetime}",
                    "prevsessionkeylifetime": f"{get_value_of_setting.prevsessionkeylifetime}",
                    "hsts": f"{get_value_of_setting.hsts}",
                    "maxage": f"{get_value_of_setting.maxage}",
                    "includesubdomains": f"{get_value_of_setting.includesubdomains}",
                    "wrong_entry_for_real": f"{get_value_of_setting.includesubdomains}",
                    "skipclientcertpolicycheck": f"{get_value_of_setting.skipclientcertpolicycheck}",

                }
            }

            # Start comparison
            return self.SSL_Profile_Compare_Settings(ns_session, current_ssl_profile_values, ServerName)

        except Exception as error:

            errormessage = ("Error Update_SSL_Profile: " + str(error.args))
            print(errormessage)

    def SSL_Profile_Compare_Settings(self, ns_session, current_ssl_profile_values, ServerName):
        try:
            # Convert dict to json
            # json_current_ssl_profile_values = json.loads(current_ssl_profile_values, sort_keys=True)

            # Get template data to compare actual data with
            json_ssl_profile_template_file = open(
                f'.\\Template\\SSL Profiles\{self.Selected_Template}')
            template_ssl_profile_values = json.load(
                json_ssl_profile_template_file)
            # Generate DeepDiff list (comparison) of current and template values
            Results = DeepDiff(current_ssl_profile_values,
                               template_ssl_profile_values)

            # Create temporary lists for later zipping, temporarily holding loop results
            hostname = []
            settings = []
            old_value = []
            new_value = []
            # create lists as required, a bit of cleaning up needs to be done on the DeepDiff result
            for x in Results['values_changed'].items():
                for y in x:
                    if type(y) == (str):

                        setting = re.sub("^root\['sslprofile']\['|']", '', y)
                        settings.append(setting)

                    else:
                        for current_set_value in y.values():
                            hostname.append(ServerName)
                            old_value.append(y['old_value'])
                            new_value.append(y['new_value'])
                            break

            comparison_list_zipped = zip(
                hostname, settings, old_value, new_value)
            comparison_list = list(comparison_list_zipped)

            return comparison_list

        except Exception as error:

            errormessage = ("Error Update_SSL_Profile: " + str(error.args))
            print(errormessage)


class FixIssues():

    def FixSelectedIssues(self, ns_session, selected_issues_to_fix):
        for i in selected_issues_to_fix:
            ServerName, setting, new_value = i['hostname'], i['setting'], i['new_value']
            print(ServerName, setting, new_value)
            # assign selected settings their template values
            try:

                profile_entry = sslprofile()
                profile_entry.name = f"{ServerName}_Turbo_ADC_Profile"
                conversion_string = f"profile_entry.{setting} = '{new_value}'"
                exec(conversion_string)

                profile_entry.update(ns_session, profile_entry)

            except Exception as error:
                errormessage = ("Error: " + str(error.args))
                print(errormessage)
