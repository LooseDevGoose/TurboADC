# ACTK_ReportFunctionality will generate either the normal or health report and convert this to a file

###############
####Imports####
###############
# Import Report Tooling

import pandas as pd
import jinja2


# Import Netscaler Nitro libs
from nssrc.com.citrix.netscaler.nitro.resource.config.lb.lbvserver import lbvserver
from nssrc.com.citrix.netscaler.nitro.resource.config.cs.csvserver import csvserver
from nssrc.com.citrix.netscaler.nitro.resource.config.vpn.vpnvserver import vpnvserver
from nssrc.com.citrix.netscaler.nitro.resource.config.authentication.authenticationvserver import authenticationvserver
from nssrc.com.citrix.netscaler.nitro.resource.config.gslb.gslbvserver import gslbvserver

# Import DateTime
from datetime import datetime

# Import OS Path
import os

###############
###/Imports/###
###############


# defines current OS path
cwd = os.getcwd()

# Class for generating a Virtual Server Report


class Create_Virtual_Server_Report():

    # Generate report based on all checkboxes ticked
    # Adds data to entry types which then parses to 'Generate Report'
    def Report_Get_Data_For_Selected_Checkbox(self, ns_session, checkboxes):

        # Entry types for 'Generate Report' syntax
        nameentries = []
        ipentries = []
        typeentries = []

        for box in checkboxes:

            # LBR Checkbox Active? Do:
            if (box.active == True and box == (checkboxes[0])):
                result = lbvserver.get(ns_session)

                # Get Index Number, LB.Name + LB. IP
                for i in (range(0, len(result))):

                    nameentries.append(result[i].name)
                    ipentries.append(result[i].ipv46)
                    typeentries.append("Load Balancing Virtual Server")

            # Content Switching Checkbox Active? Do:
            elif (box.active == True and box == (checkboxes[1])):
                result = csvserver.get(ns_session)
                for i in (range(0, len(result))):

                    nameentries.append(result[i].name)
                    ipentries.append(result[i].ipv46)
                    typeentries.append("Content Switching Virtual Server")

            # VPN/Gateway Checkbox Active? Do:
            elif (box.active == True and box == (checkboxes[2])):
                result = vpnvserver.get(ns_session)
                for i in (range(0, len(result))):
                    nameentries.append(result[i].name)
                    ipentries.append(result[i].ipv46)
                    typeentries.append("VPN Virtual Server")
            # AAA Checkbox Active? Do:
            elif (box.active == True and box == (checkboxes[3])):
                result = authenticationvserver.get(ns_session)
                for i in (range(0, len(result))):
                    nameentries.append(result[i].name)
                    ipentries.append(result[i].ipv46)
                    typeentries.append("Authentication Virtual Server")

            # GSLB Checkbox Active? Do:
            elif (box.active == True and box == (checkboxes[4])):
                result = gslbvserver.get(ns_session)
                for i in (range(0, len(result))):
                    nameentries.append(result[i].name)
                    ipentries.append(result[i].ipv46)
                    typeentries.append("GSLB Virtual Server")

        GenerateReportInstantiator = Print_Report_To_HTML()
        GenerateReportInstantiator.GenerateReport(
            nameentries, ipentries, typeentries)

# Class for generating a Virtual Server Health Report


class Generate_Virtual_Server_Health_Report():

    def HealthReportCheckboxes(ns_session, checkboxes):

        pass


class Print_Report_To_HTML():

    # Reporting Functionality done with Pandas for Report Checkboxes
    def GenerateReport(self, nameentries, ipentries, typeentries):
        df = pd.DataFrame(zip(nameentries, ipentries, typeentries), columns=[
                          'Name', 'IP', 'Type'])

        # See: https://pandas.pydata.org/pandas-docs/stable/user_guide/style.html#Building-styles
        def color_negative_red(val):
            color = 'black'
            return f'color: {color}'

        styler = df.style.applymap(color_negative_red)

        cwdtemplate = cwd + '\\Template\HtmlTemplates'

        # Template handling
        env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(searchpath=f'{cwdtemplate}'))
        template = env.get_template('template.html')
        html = template.render(my_table=styler.render())

        # Writing of file

        # Define Date/Time to use in name string
        now = datetime.now()
        dt_string = str(now.strftime("%d-%m-%Y %Hh%Mm%Ss"))

        # Get current path and add \\Reports to the string
        cwdreport = cwd + '\\Reports'

        # Write report in raw (r) to support path, it writes to the 'reports' folder in the same dir
        with open(fr"{cwdreport}\{dt_string}.html", 'w') as f:
            f.write(html)

        # place code here for when file is done writing Hooray!

        # Open explorer to see file
        os.startfile(fr'"{cwdreport}"')
