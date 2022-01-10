# This file is mainly used to create the UI in combination with the KV file.
# The UI consists of 'screens' whom have their own functionality
# Screen functionality gets sent to different files e.g. ADCTK_ReportFunctionality or ADCTK_SecurityScan
# When functionality is done, data gets fed back to the screen and shown to user

# Please mind that the draw time of the screen impacts what is shown, as it does not update dynamically

###############
####Imports####
###############

# Import OS
import os
from os import listdir
from os.path import isfile, join
from kivy.uix import recycleview

# Import Kivy libraries
from kivymd.app import MDApp
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.properties import StringProperty
from kivy.properties import NumericProperty
from kivy.properties import BooleanProperty
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior


# Import Dialog libraries
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton

# Import DataTable Libs
from kivymd.uix.datatables import MDDataTable

# Import DropDown Libs
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.list import OneLineIconListItem

# Import List Libaries
from kivymd.uix.list import IRightBodyTouch, OneLineAvatarIconListItem
from kivymd.uix.selectioncontrol import MDCheckbox

# Required for specfile for some reason
# Can't generate .exe without this (might need to check again)
from kivymd.effects import stiffscroll

# Import Scripts File
import ADCTK_SecurityScan
import ADCTK_ReportFunctionality

# Libraries from Netscaler Nitro API
from nssrc.com.citrix.netscaler.nitro.service.nitro_service import nitro_service
###############
###/Imports/###
###############

####################
###Custom Classes###
####################


class Dialog_Requesting_Public_IP_And_Hostname(Screen):
    pass


# Define Custom List Items for SSLReport Create_List()


class ListItemWithCheckbox(RecycleDataViewBehavior, OneLineAvatarIconListItem):
    '''Custom list item.'''
    icon = StringProperty("android")
    hostname = StringProperty("")
    setting = StringProperty("")
    old_value = StringProperty("")
    new_value = StringProperty("")
    activated = BooleanProperty()
    index = NumericProperty()

    def update_active(self, index, data):
        for entry in data:
            if entry['index'] == index:
                if entry['activated'] == True:
                    entry['activated'] = False
                    return(False)
                else:
                    entry['activated'] = True
                    return(True)

    def refresh_view_attrs(self, rv, number, data):
        ''' Catch and handle the view changes '''
        if data['activated'] == True:
            self.ids.cb.active = True
        else:
            self.ids.cb.active = False

        return super(ListItemWithCheckbox, self).refresh_view_attrs(
            rv, number, data)


class RightCheckbox(IRightBodyTouch, MDCheckbox):
    '''Custom right container.'''


# Define custom class for MDDropDownMenu


class IconListItem(OneLineIconListItem):
    pass


class RV(RecycleView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = []

    def checkbox_callback(self, btn, index):
        for entry in self.data:
            if entry['index'] == index:
                if entry['activated'] == True:
                    entry['activated'] = False

                    return(False)
                else:
                    entry['activated'] = True

                    return(True)

        print(btn, btn.active)


####################
###/Custom Classes/###
####################

# Window Manager


class WindowManager(ScreenManager):
    pass


class LoginScreen(Screen):

    def submitinfo(self):

        global nsip
        global nsusername

        nsip = self.ids.ns_ip.text
        nsusername = self.ids.ns_username.text
        nspassword = self.ids.ns_password.text

        try:
            global ns_session
            ns_session = nitro_service(f"{nsip}", "http")
            ns_session.login(f"{nsusername}", f"{nspassword}", 3600)
            return (ns_session.isLogin())

        except Exception as error:

            errormessage = ("Error: " + str(error.args))
            self.ids.error_label_login.text = errormessage

    def cleardata(self):
        self.ids.ns_ip.text = ("")
        self.ids.ns_username.text = ("")
        self.ids.ns_password.text = ("")


class MainMenu(Screen):

    def on_pre_enter(self):
        self.ids.welcomename.text = (f"Welcome, {nsusername}")
        self.ids.welcomeip.text = (f"You are logged in on ADC with IP: {nsip}")

    # Handles open/closing of the NavRail
    def rail_open(self):
        if self.ids.navrail.rail_state == "open":
            self.ids.navrail.rail_state = "close"
        else:
            self.ids.navrail.rail_state = "open"

    # Sets all checkboxes and passes them to the reporting feature in ADCTK_NitroLogin

    def Create_Report_Selected_Servers(self):

        checkboxes = [
            self.ids.LBRCheckbox, self.ids.CSRCheckbox, self.ids.VPNRCheckbox,
            self.ids.AAARCheckbox, self.ids.GSLBRCheckbox
        ]
        ReportInstantiator = ADCTK_ReportFunctionality.Create_Virtual_Server_Report(
        )
        ReportInstantiator.Report_Get_Data_For_Selected_Checkbox(
            ns_session, checkboxes)

    # Sets all checkboxes and passed them to the health check feature in ADCTK_NitroLogin

    def GetHealthServers(self):

        checkboxes = [
            self.ids.LBHCheckbox,
            self.ids.CSHCheckbox,
        ]


# Screen for Security DataTable


class Security_Scan_Virtual_Server_Table_Screen(Screen):

    # Define dict for virtual servers
    VirtualServerDict = {}

    # When screen opens this code executes:
    def on_pre_enter(self):

        # Instantiates Class's function
        Table_Data_Filler = ADCTK_SecurityScan.Fill_Data_Table_With_Virtual_Servers(
        )

        # Populates DataTable columns data
        columns = Table_Data_Filler.Set_Column_Data()
        rows = Table_Data_Filler.Set_Row_Data(ns_session)

        # Populate DataTable / Settings
        self.data_tables = MDDataTable(pos_hint={
            'center_y': 0.5,
            'center_x': 0.5
        },
            size_hint=(0.98, 0.75),
            use_pagination=False,
            rows_num=len(rows),
            check=True,
            column_data=columns,
            row_data=rows)
        self.data_tables.bind(on_check_press=self.on_check_press)
        # Add DataTable to screen
        self.add_widget(self.data_tables)

    # Gets files from template folder and adds to list
    def Get_SSL_Templates(self):

        self.TemplateList = []
        cwd = os.getcwd()
        mypath = cwd + '\\Template\SSL Profiles'
        files = os.listdir(mypath)

        for f in files:
            self.TemplateList.append({
                "text":
                f"{f}",
                "viewclass":
                "IconListItem",
                "on_release":
                lambda x=f"{f}": self.set_item(x),
            })

        self.menu = MDDropdownMenu(
            caller=self.ids.dropdown_item,
            items=self.TemplateList,
            position="auto",
            width_mult=8,
        )
        return self.menu.bind()

    def set_item(self, text_item):
        self.ids.dropdown_item.text = f"{text_item}"
        self.menu.dismiss()
        self.Selected_Template = text_item

    # When checkbox is pressed get the 2nd and 4th column information and add to variable
    def on_check_press(self, instance_table, current_row):

        # Contains row Index Number
        vindex, vname, vip, vtype = current_row[0], current_row[
            1], current_row[2], current_row[3]

        # use global variable for tricky function (grabtext)
        self.vname = vname

        # Prevent double entries in list by reclicking checkbox and adding data
        if f'{vname}' not in self.VirtualServerDict:
            # Create dictionary key with the above variables
            self.VirtualServerDict[f"{vname}"] = [
                f"{vname}", f"{vip}", f"{vtype}"
            ]

        # Remove Entries from list on uncheck if entry name present
        elif f'{vname}' in self.VirtualServerDict:
            self.VirtualServerDict.pop(f"{vname}")

    # Remove widget upon leaving screen (cleanup)
    def on_leave(self):

        self.remove_widget(self.data_tables)
        self.VirtualServerDict = {}

    # Parse the dictionary/list with all data to Next screen (SSL Report)
    def startCheck(self):

        global Public_Vserver_Dict
        Public_Vserver_Dict = self.VirtualServerDict
        global Selected_SSL_Template
        Selected_SSL_Template = self.Selected_Template


# Parse information to SSL labs API and return results in listview with checkboxes


class Generate_Security_Scan_Results(Screen):

    def on_pre_enter(self):
        Vulnerabilities = self.create_list(Public_Vserver_Dict)
        self.create_entries(Vulnerabilities)

    # Create a list with issues found in the report, convert these to checkboxlistitem

    def create_list(self, Public_Vserver_Dict):

        # Amount of servers to check
        count = 0
        Vulnerabilitylist = []
        # Iterate through Virtual Server Dict and assign hostname/ip to submit to ADCTK_SecurityScan
        for i in Public_Vserver_Dict:
            count += 1
            Virtual_Server_Name = Public_Vserver_Dict[i][0]

            if count == 1:
                # Set Titel Label to VserverName
                self.ids.vserverlabel.text = Virtual_Server_Name

            elif count >= 2:
                # If more than 1 servers selected, adjust vanity text
                self.ids.vserverlabel.text = "Multiple Servers selected. Spicy."

            elif count >= 10:
                # If more than 9 servers selected, adjust vanity text
                self.ids.vserverlabel.text = "Bulk Scan detected, Bring the heat baby!"

            # instantiate ADCTK_SecurityScan
            i = ADCTK_SecurityScan.SSL_Hardening_Procedure()
            # Start report check with given hostname
            convert_list = []
            convert_list.append(i.Check_If_SSL_Profile_Present(
                Virtual_Server_Name, ns_session, Selected_SSL_Template))

            for x in convert_list:
                if x is not None:
                    Vulnerabilitylist.append(x)

        return (Vulnerabilitylist)

    def create_entries(self, Vulnerabilities):
        try:
            # Define amount of issues
            i = 0

            # self.recycleview = RV()
            # For each Vulnerability discovered, create list item with name
            for y in Vulnerabilities:

                for x in y:
                    i += 1
                    key = (
                        f"Hostname: '{x[0]}' has value '{x[1]}' set to '{x[2]}' and it should be '{x[3]}'")

                    self.ids.rvs.data.append({'text': f"{key}", 'hostname': str(x[0]),
                                              'setting': str(x[1]), 'old_value': str(x[2]), 'new_value': str(x[3]), 'icon': "alert-circle-outline", 'activated': True, 'index': i})

            # Add RecycleView to screen (required to optimize when using lots of entries)
            # self.ids.container.add_widget(self.recycleview)

            # Set label to equal amount of issues
            if i == 1:
                self.ids.vserverstatus.text = (
                    f"detected {i} profile mismatch")
            elif i >= 1:
                self.ids.vserverstatus.text = (
                    f"detected {i} profile mismatches")
            else:
                self.ids.vserverstatus.text = (
                    "No profile mismatches detected :)")

        except Exception as error:
            errormessage = ("Error creating entries for SSL comparison: " +
                            str(error.args))
            print(errormessage)

    # Solves issues selected based on selection

    def save_checked(self):
        # Variable for assigning names of selected issues
        selected_issues_to_fix = []

        activated_list = self.ids.rvs.data
        for entry in activated_list:
            if entry['activated'] == True:
                # instantiate code here
                selected_issues_to_fix.append(entry)
        print(selected_issues_to_fix)

        Instantiate = ADCTK_SecurityScan.FixIssues()
        Instantiate.FixSelectedIssues(ns_session, selected_issues_to_fix)
        self.dialog = MDDialog(text="All done!",
                               buttons=[MDFlatButton(text="OK", )])
        self.dialog.open()

    def on_leave(self):
        self.remove_widget(self.ids.rvs)
        self.ids.rvs.data = []

        # Build Class for Login Screen inc. Theme data


class mhtk(MDApp):

    def build(self):
        Window.size = (1200, 800)
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.hue = 700
        self.icon = "Images/Logo.png"
        self.title = "MHTK 1.0.0"

    def change_screen(self, screen: str):
        self.root.current = screen


def runMHTK():
    mhtk().run()
