# Z library
import wx
from wx.lib import scrolledpanel
from PIL import Image
import io
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import pyscreenshot
import win32gui


class PanelBase(wx.Panel):
    def __init__(self, parent, label, on_click):
        super(PanelBase, self).__init__(parent, id=-1)
        self.parent_frame = parent
        self.SetSize(704, 421)


class MainPanel(PanelBase):
    def __init__(self, parent, on_click):
        super(MainPanel, self).__init__(parent, 'MainPanel', on_click)
        self.width, self.height = 704, 421
        self.on_click = on_click
        self.Main_UI()

    def Main_UI(self):
        # init contents
        self.font1 = wx.Font(15, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Times New Roman')
        self.main_panel_sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.main_panel_sizer)

        self.search_sub_sizer_1 = wx.BoxSizer(wx.HORIZONTAL)
        self.search_sub_sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        self.recom_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.logo_image = wx.Image(r'.\\Resources\\icons\\lib-logo.png')
        self.logo_image = self.logo_image.Rescale(width=220, height=80, quality=wx.IMAGE_QUALITY_NORMAL)

        self.search_panel = wx.Panel(self, id=-1, size=(self.width, int(3 * self.height / 10)), pos=(0, 0),
                                     style=wx.SIMPLE_BORDER)
        self.search_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.search_panel.SetSizer(self.search_sizer)

        self.search_panel.SetSizer(self.search_sizer)

        self.search_sizer.Add(self.search_sub_sizer_1, 5, wx.EXPAND, 15)
        self.search_sizer.Add(self.search_sub_sizer_2, 5, wx.EXPAND, 15)

        self.recom_panel = scrolledpanel.ScrolledPanel(self, id=-1, size=(self.width, int(7 * self.height / 10)),
                                                       pos=(0, int(3 * self.height / 10)),
                                                       style=wx.TAB_TRAVERSAL)
        print(self.search_panel.GetSize())
        self.recom_panel.SetupScrolling()
        self.recom_panel.SetSizer(self.recom_sizer)

        # initialize scraping
        self.url = "https://1lib.in/"
        hdr = {'User-Agent': 'Mozilla/5.0'}
        req = Request(self.url, headers=hdr)
        self.page = urlopen(req)
        self.page_read = self.page.read()
        self.page.close()
        self.page_soup = BeautifulSoup(self.page_read, features='html.parser')

        self.logo = wx.BitmapButton(self.search_panel, id=-1, bitmap=wx.Bitmap(self.logo_image), size=(230, 100),
                                    pos=(50, 0))
        self.search_sub_sizer_1.Add(self.logo, 0, wx.LEFT | wx.ALIGN_CENTER_VERTICAL, 25)

        self.search_box = wx.TextCtrl(self.search_panel, id=-1, value="", size=(300, 25),
                                      style=wx.TE_PROCESS_ENTER)
        self.search_box.SetFont(self.font1)
        self.search_box.Bind(wx.EVT_TEXT_ENTER, self.on_click)
        self.search_sub_sizer_2.Add(self.search_box, 0, wx.ALIGN_CENTER_VERTICAL)

        self.search_logo = wx.Image(r'.\\Resources\\icons\\search-logo.png')
        self.search_logo = self.search_logo.Rescale(width=35, height=35, quality=wx.IMAGE_QUALITY_NORMAL)
        self.search_button = wx.BitmapButton(self.search_panel, id=-1, bitmap=wx.Bitmap(self.search_logo),
                                             size=(35, 35))
        self.search_button.Bind(wx.EVT_BUTTON, self.on_click)
        self.search_sub_sizer_2.Add(self.search_button, 0, wx.ALIGN_CENTER_VERTICAL)

        self.main_panel_sizer.Add(self.search_panel, 0, wx.ALL)
        self.main_panel_sizer.Add(self.recom_panel, 0, wx.ALL)

        self.recom_UI()

    def recom_UI(self):
        self.recom_list = [None] * 20
        self.def_image = wx.Image(r".\\Resources\\icons\\book-icon.png")

        for x in range(20):
            self.recom_list[x] = wx.BitmapButton(self.recom_panel, id=-1, bitmap=wx.Bitmap(self.def_image),
                                                 size=(161, 250), style=wx.BU_NOTEXT)
            self.recom_sizer.Add(self.recom_list[x], 0, wx.ALL, 5)

        self.recom_panel.Refresh()
        self.recom_panel.Show()
        self.scrape_recom()

    def request_filled(self):
        print("Class passed")

    def scrape_recom(self):
        self.containers = self.page_soup.find_all('div', class_='brick checkBookDownloaded')
        print(len(self.containers))
        x = 0
        for container in self.containers:
            print(container.a['href'])
            print(container.a['title'])
            width, height = self.recom_list[x].GetSizeTuple()
            self.recom_list[x].SetToolTip(wx.ToolTip(container.a['title']))
            self.recom_list[x].SetLabel("https://1lib.in" + str(container.a['href']))
            self.recom_list[x].Bind(wx.EVT_BUTTON, self.on_click)
            self.img_stream = io.BytesIO(urlopen(Request(container.a.img['src'])).read())
            self.image_buff = wx.Image(self.img_stream)
            self.image_buff = self.image_buff.Rescale(width, height, wx.IMAGE_QUALITY_NORMAL)
            self.recom_list[x].SetBitmap(wx.Bitmap(self.image_buff))
            x += 1


class LogoPanel(PanelBase):
    def __init__(self, parent, on_click):
        super(LogoPanel, self).__init__(parent, 'LogoPanel', on_click)


class DetailPanel1(PanelBase):
    def __init__(self, parent, on_click):
        super(DetailPanel1, self).__init__(parent, 'DetailPanel1', on_click)
        self.width, self.height = 704, 421
        self.SetSize(self.width, self.height)
        self.on_click = on_click

        self.main_scrape_UI_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(self.main_scrape_UI_sizer)
        self.def_image = wx.Image(r".\\Resources\\icons\\book-icon.png")

        self.detail_panel = wx.Panel(self, id=-1, size=(int(self.width / 2) + 90, self.height), style=wx.BORDER_NONE)
        self.detail_sizer = wx.BoxSizer(wx.VERTICAL)
        self.detail_panel.SetSizer(self.detail_sizer)
        self.main_scrape_UI_sizer.Add(self.detail_panel)
        self.index_panel = scrolledpanel.ScrolledPanel(self, id=-1, size=(int(self.width / 2) - 90, self.height),
                                                       style=wx.TE_BESTWRAP)
        self.main_scrape_UI_sizer.Add(self.index_panel)

        self.detail_sub_panel_11 = wx.Panel(self.detail_panel, id=-1,
                                            size=(int(self.width / 2) + 90, (self.height / 2) - 30),
                                            style=wx.NO_BORDER)
        self.detail_sub_panel_11_sizer = wx.BoxSizer(wx.HORIZONTAL)
        print(self.detail_sub_panel_11.GetClientSize())
        self.detail_sub_panel_11.SetSizer(self.detail_sub_panel_11_sizer)

        self.detail_sub_panel_12 = wx.Panel(self.detail_panel, id=-1,
                                            size=(int(self.width / 2) + 90, (self.height / 2) + 30),
                                            style=wx.NO_BORDER)
        self.detail_sub_panel_12_sizer = wx.BoxSizer(wx.VERTICAL)
        self.detail_sub_panel_12.SetSizer(self.detail_sub_panel_12_sizer)

        self.detail_sizer.Add(self.detail_sub_panel_11)
        self.detail_sizer.Add(self.detail_sub_panel_12)

        # sun sizer 1
        self.book_bitmap = wx.BitmapButton(self.detail_sub_panel_11, id=-1, size=(120, int((2 * self.height) / 5)),
                                           bitmap=wx.Bitmap(self.def_image), style=wx.BU_BOTTOM)
        self.detail_sub_panel_11_sizer.Add(self.book_bitmap, 0, wx.LEFT | wx.TOP | wx.BOTTOM, 5)

        self.book_detail_panel = wx.Panel(self.detail_sub_panel_11, id=-1, size=(310, int((2 * self.height) / 5)),
                                          style=wx.NO_BORDER)
        self.detail_sub_panel_11_sizer.Add(self.book_detail_panel, 0, wx.ALL, 5)
        self.book_detail_sizer = wx.BoxSizer(wx.VERTICAL)
        self.book_detail_panel.SetSizer(self.book_detail_sizer)

        self.font2 = wx.Font(14, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Arial')
        self.font3 = wx.Font(9, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Roboto')
        self.font4 = wx.Font(12, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Roboto')

        self.book_detail_sizer_1 = wx.BoxSizer(wx.HORIZONTAL)
        self.book_detail_sizer_2 = wx.BoxSizer(wx.HORIZONTAL)

        # book  details scraped
        self.book_name = wx.StaticText(self.book_detail_panel, id=-1, label="Book")
        self.book_name.SetFont(self.font2)
        self.book_isbn = wx.StaticText(self.book_detail_panel, id=-1, label="ISBN: ")
        self.book_isbn_10 = wx.StaticText(self.book_detail_panel, id=-1, label="ISBN 10: ")
        self.book_isbn_13 = wx.StaticText(self.book_detail_panel, id=-1, label="ISBN 13: ")
        self.book_author = wx.StaticText(self.book_detail_panel, id=-1, label="Author: ")
        self.pages = wx.StaticText(self.book_detail_panel, id=-1, label="    No. of pages: ")
        self.book_category = wx.StaticText(self.book_detail_panel, id=-1, label="Publisher: ")
        self.file_type = wx.StaticText(self.book_detail_panel, id=-1, label="File: ")
        self.pub_year = wx.StaticText(self.book_detail_panel, id=-1, label="    Year: ")

        self.book_detail_sizer.Add(self.book_name, 0, flag=wx.TOP | wx.LEFT, border=5)
        self.book_detail_sizer.Add(self.book_isbn, flag=wx.TOP | wx.LEFT, border=5)
        self.book_detail_sizer.Add(self.book_isbn_10, flag=wx.TOP | wx.LEFT, border=5)
        self.book_detail_sizer.Add(self.book_isbn_13, flag=wx.TOP | wx.LEFT, border=5)
        self.book_detail_sizer_1.Add(self.book_author, 0)
        self.book_detail_sizer_1.Add(self.pages, 0, flag=wx.RIGHT, border=10)
        self.book_detail_sizer.Add(self.book_detail_sizer_1, flag=wx.TOP | wx.LEFT, border=5)
        self.book_detail_sizer.Add(self.book_category, flag=wx.TOP | wx.LEFT, border=5)
        self.book_detail_sizer_2.Add(self.file_type)
        self.book_detail_sizer_2.Add(self.pub_year, flag=wx.RIGHT, border=10)
        self.book_detail_sizer.Add(self.book_detail_sizer_2, flag=wx.TOP | wx.LEFT, border=5)

        self.x = " " * 15

        self.descrip_label = wx.StaticText(self.detail_sub_panel_12, id=-1, label=self.x + "DESCRIPTION")
        self.descrip_label.SetFont(self.font4)
        self.book_description = wx.TextCtrl(self.detail_sub_panel_12, id=-1, value="",
                                            size=(int(self.width / 2) + 90, (self.height / 2) + 10),
                                            style=wx.TE_MULTILINE)
        self.book_description.SetFont(self.font3)

        self.detail_sub_panel_12_sizer.Add(self.descrip_label)
        self.detail_sub_panel_12_sizer.Add(self.book_description)

        self.main_list_sizer = wx.GridSizer (cols=2, vgap=5, hgap=5)
        self.index_panel.SetSizer(self.main_list_sizer)

    def scrape_detail(self, url):
        # init contents
        self.url_passed = url

        # initialize scraping
        hdr = {'User-Agent': 'Mozilla/5.0'}
        request = Request(self.url_passed, headers=hdr)
        self.page_hex = urlopen(request)
        self.page_code = self.page_hex.read()
        self.page_hex.close()
        self.page_analytic = BeautifulSoup(self.page_code, features='html.parser')

        self.page_var = self.page_analytic.find('div', {"itemtype": "http://schema.org/Book"})
        self.b_name = self.page_var.h1.get_text().strip()
        self.b_details = self.page_var.find('div', {'class': "bookDetailsBox"})

        # details
        try:
            self.b_auth = self.page_analytic.find('div', {'class': "col-sm-9"}).i.get_text()
            print(self.b_auth)
        except AttributeError:
            self.b_auth = "--"

        try:
            self.b_isbn10 = self.b_details.find('div', {'class': "bookProperty property_isbn 10"}).find('div', {
                'class': "property_value"}).get_text()
            print(self.b_isbn10)
        except AttributeError:
            self.b_isbn10 = "--"

        try:
            self.b_isbn = self.b_details.find('div', {'class': "bookProperty property_isbn"}).find('div', {
                'class': "property_value"}).get_text()
            print(self.b_isbn)
        except AttributeError:
            self.b_isbn = "--"

        try:
            self.b_isbn13 = self.b_details.find('div', {'class': "bookProperty property_isbn 13"}).find('div', {
                'class': "property_value"}).get_text()
            print(self.b_isbn13)
        except AttributeError:
            self.b_isbn13 = "--"

        self.b_year = self.b_details.find('div', {'class': "bookProperty property_year"}).find('div', {
            'class': "property_value"}).get_text()
        print(self.b_year)

        try:
            self.b_pages = self.b_details.find('div', {'class': "bookProperty property_pages"}).find('div', {
                'class': "property_value"}).span.get_text()
            print(self.b_pages)
        except AttributeError:
            self.b_pages = "--"

        self.b_type = self.b_details.find('div', {'class': "bookProperty property__file"}).find('div', {
            'class': "property_value"}).get_text()
        print(self.b_type)

        try:
            self.b_pub = self.b_details.find('div', {'class': "bookProperty property_publisher"}).find('div', {
                'class': "property_value"}).get_text()
            print(self.b_pub)
        except AttributeError:
            self.b_pub = "--"

        self.content_group = self.page_analytic.find ('div', {'id': "bookDescriptionBox"})
        self.content_truth = False
        self.b_descrip = " "

        try:
            self.content = self.content_group.find_all('span')
        except AttributeError:
            print("First Test failed")
            self.content=[]
            self.content_truth = False

        if not self.content_truth:
            try:
                print("Second Try")
                self.content = self.content_group.find_all('p')
                if self.content:
                    self.content_truth = True
                    for text in self.content:
                        self.b_descrip = self.b_descrip + str(text.get_text()) + "\n"
            except AttributeError:
                self.b_descrip = "--No Description Found--"
                print("Test 2 failed!!")
        else:
            for text in self.content:
                self.b_descrip = self.b_descrip + str(text.get_text()) + "\n"
            self.content_truth = True
            print("Content test successful")

        if not self.content_truth:
            try:
                print("Third test")
                self.content = self.content_group.get_text()
                self.b_descrip = " "
                if self.content:
                    self.b_descrip = self.b_descrip + self.content.string
            except AttributeError:
                self.b_descrip = "--No Description Found--"


        self.b_map = io.BytesIO(
            urlopen(Request(self.page_analytic.find('div', {'class': "col-sm-3"}).a.img['src'])).read())
        self.b_buffer = wx.Image(self.b_map).Rescale(width=120, height=int((2 * self.height) / 5),
                                                     quality=wx.IMAGE_QUALITY_NORMAL)

        self.book_bitmap.SetBitmap(wx.Bitmap(self.b_buffer))

        self.book_name.SetLabel(self.b_name)
        self.book_name.SetToolTip(wx.ToolTip(self.b_name))
        self.book_isbn.SetLabel("ISBN: "+self.b_isbn)
        self.book_isbn_10.SetLabel("ISBN 10: "+self.b_isbn10)
        self.book_isbn_13.SetLabel("ISBN 13: "+self.b_isbn13)
        self.book_author.SetLabel("Author: "+self.b_auth)
        self.pages.SetLabel("    No. of pages: " + self.b_pages)
        self.book_category.SetLabel("Publisher: " + self.b_pub)
        self.file_type.SetLabel("File: " + self.b_type)
        self.pub_year.SetLabel("    Year: " + self.b_year)
        self.book_description.SetValue (self.b_descrip)

        self.detail_panel.Layout()


        self.onmainpanelclick()


    def onmainpanelclick(self):

        self.children = self.main_list_sizer.GetChildren()

        i = len(self.children)-1

        if len(self.children) != 0:
            while i >= 0:
                win = self.main_list_sizer.GetItem(0).GetWindow()
                win.Destroy()
                i -= 1
            self.main_list_sizer.Layout()
        else:
            print("Empty")

        self.containers = self.page_analytic.find_all('div', {'class': "brick checkBookDownloaded"})
        print(self.containers)

        self.button_spec_1 = [None] * len(self.containers)
        print("Dynamic length: "+str(len(self.containers)))
        i = 0

        for container in self.containers:
            self.url_param = container.a['href']
            self.buffer = wx.Image(io.BytesIO(urlopen(Request(container.a.img['src'])).read()))
            self.buffer = self.buffer.Rescale(width=120, height=int((2 * self.height) / 5),
                                              quality=wx.IMAGE_QUALITY_HIGH)
            self.button_spec_1[i] = wx.BitmapButton(self.index_panel, id=-1, size=(120, int((2 * self.height) / 5)),
                                                    bitmap=wx.Bitmap(self.buffer), style=wx.BU_NOTEXT)
            self.button_spec_1[i].SetLabel("https://1lib.in"+ self.url_param)
            self.button_spec_1[i].Bind(wx.EVT_BUTTON, self.on_click)
            self.main_list_sizer.Add(self.button_spec_1[i])
            self.button_spec_1[i].SetToolTip(wx.ToolTip(container.a['title']))
            i += 1

        self.index_panel.SetupScrolling()
        self.index_panel.Bind(wx.EVT_MOTION, self.OnMouse)
        self.index_panel.Layout()
        self.Layout()

    def OnMouse(self, event):
        self.index_panel.SetFocus()


class DetailPanel2(PanelBase):
    def __init__(self, parent, on_click):
        super(DetailPanel2, self).__init__(parent, 'DetailPanel2', on_click)
        self.width, self.height = 704, 421
        self.on_click = on_click
        self.font1 = wx.Font(10, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Calibri')
        self.font2 = wx.Font(10, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Lucida Console')

        self.go_img = wx.Image(r".\\Resources\\icons\\go_to.png")
        self.go_img = self.go_img.Rescale(width=28, height=28, quality=wx.IMAGE_QUALITY_HIGH)
        self.next_node = wx.Image(r".\\Resources\\icons\\drop_down.png")
        self.next_node = self.next_node.Rescale(width=16, height=16, quality=wx.IMAGE_QUALITY_HIGH)

        self.next_page = wx.Image(r".\\Resources\\icons\\next.png")
        self.next_page = self.next_page.Rescale(width=28, height=28, quality=wx.IMAGE_QUALITY_HIGH)

        self.prev_page = wx.Image(r".\\Resources\\icons\\prev.png")
        self.prev_page = self.prev_page.Rescale(width=28, height=28, quality=wx.IMAGE_QUALITY_HIGH)

        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.main_sizer)

        self.bottom_panel_list = list()
        self.page_index = 1
        self.list_counter = 0

        self.MainUI()

    def MainUI(self):
        # top panel
        self.main_top_panel = wx.Panel(self, id=-1, size=(self.width, self.height / 10), pos=(0, 0),
                                       style=wx.SIMPLE_BORDER)
        self.main_top_panel_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.main_top_panel.SetSizer(self.main_top_panel_sizer)
        self.search_box = wx.TextCtrl(self.main_top_panel, id=-1, value="", size=(400, 20),
                                      style=wx.TE_LEFT | wx.TE_PROCESS_ENTER)
        self.search_box.SetFont(self.font1)
        self.search_box.Bind(wx.EVT_TEXT_ENTER, self.on_click)
        self.search_button = wx.BitmapButton(self.main_top_panel, id=-1, bitmap=wx.Bitmap(self.go_img),
                                             size=(20, 20), style=wx.BU_LEFT)
        self.next_arrow = wx.BitmapButton(self.main_top_panel, id=-1, bitmap=wx.Bitmap(self.next_page),
                                          size=(30, 30), style=wx.BU_NOTEXT)
        self.next_arrow.Bind(wx.EVT_BUTTON, self.on_list1)

        self.prev_arrow = wx.BitmapButton(self.main_top_panel, id=-1, bitmap=wx.Bitmap(self.prev_page),
                                          size=(30, 30), style=wx.BU_NOTEXT)
        self.prev_arrow.Bind(wx.EVT_BUTTON, self.on_list2)

        self.main_top_panel_sizer.Add(self.search_box, 0, wx.LEFT | wx.TOP, 10)
        self.main_top_panel_sizer.Add(self.search_button, 0, wx.LEFT | wx.TOP, 10)
        self.main_top_panel_sizer.Add(self.prev_arrow, 0, wx.LEFT, 10)
        self.main_top_panel_sizer.Add(self.next_arrow, 0, wx.LEFT, 10)
        self.main_sizer.Add(self.main_top_panel)

        # bottom panel
        self.bottom_panel = wx.Panel(self, id=-1, size=(self.width, int(9 * self.height / 10)),
                                     pos=(0, 9 * self.height / 10), style=wx.SIMPLE_BORDER)
        self.bottom_panel_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.bottom_panel.SetSizer(self.bottom_panel_sizer)
        self.main_sizer.Add(self.bottom_panel)

    def on_list1(self, event):
        self.page_index += 1
        self.list_counter += 1
        if "?page=" in self.search_box.GetValue():
            self.arg = "https://1lib.in/s/"+self.search_box.GetValue()[:-1]+str(self.page_index)
        else:
            self.arg = "https://1lib.in/s/"+self.search_box.GetValue()+ "?page="+str(self.page_index)

        self.bottom_panel_list[self.list_counter-1].Hide()
        self.list_scrape(self.arg)


    def on_list2(self, event):
        self.page_index -= 1
        self.arg = "https://1lib.in/s/" + self.search_box.GetValue() + "?page=" + str(self.page_index)
        self.list_scrape(self.arg)

    def list_scrape(self, url):
        # initialize scraping
        self.url_pick = url
        hdr = {'User-Agent': 'Mozilla/5.0'}
        req = Request(self.url_pick, headers=hdr)
        self.page = urlopen(req)
        self.page_pick = self.page.read()
        self.page.close()
        self.page_soup = BeautifulSoup(self.page_pick, features='html.parser')

        self.counter = 0
        print("Counter set to: " + str(self.counter))
        self.search_value = self.url_pick.split('/')
        self.search_box.SetValue(self.search_value[len(self.search_value) - 1])

        self.page_content = self.page_soup.find_all('td', {'style': 'vertical-align: top;'})
        print(self.page_content)
        self.scrape_creation()


    def scrape_creation(self):

        self.buffer_panel = scrolledpanel.ScrolledPanel(self.bottom_panel, id=-1,
                                                        size=(self.width, int(9 * self.height / 10)),
                                                        pos=(0, 9 * self.height / 10), style=wx.TAB_TRAVERSAL)
        self.buffer_panel_sizer = wx.BoxSizer(wx.VERTICAL)
        self.buffer_panel.SetSizer(self.buffer_panel_sizer)

        self.bottom_panel_list.append(self.buffer_panel)
        self.bottom_panel_sizer.Add(self.buffer_panel)

        self.node_list = list()


        for i in range(len(self.page_content)):
            self.content_list = self.page_content[self.counter].find_all('a')
            self.content_list2 = self.page_content[self.counter].find_all('div', {'class': "property_value"})

            self.buffer_low_panel = wx.Panel(self.buffer_panel, id=-1, size=(self.width - 30, 50),
                                             style=wx.SIMPLE_BORDER)
            self.buffer_top_sizer = wx.BoxSizer(wx.VERTICAL)
            self.buffer_low_panel.SetSizer(self.buffer_top_sizer)

            self.sub_1_sizer = wx.BoxSizer(wx.HORIZONTAL)
            self.sub_2_sizer = wx.GridSizer(cols=4, vgap=3, hgap=3)
            self.buffer_top_sizer.Add(self.sub_1_sizer)
            self.buffer_top_sizer.Add(self.sub_2_sizer)

            self.buffer = self.content_list[0].get_text()
            print(self.buffer)
            self.buff_label = wx.StaticText(self.buffer_low_panel, id=-1, label=self.buffer[:80])
            self.buff_label.SetFont(self.font2)
            self.sub_1_sizer.Add(self.buff_label, 0, wx.LEFT | wx.TOP, 5)
            self.buffer = self.content_list[1].get_text()[:25]
            print(self.buffer)
            self.buff_auth = wx.StaticText(self.buffer_low_panel, id=-1, label="By: " + str(self.buffer))
            self.sub_2_sizer.Add(self.buff_auth, 0, wx.LEFT | wx.ALIGN_CENTER_VERTICAL, 20)
            self.buffer = self.content_list2[0].get_text()
            print(self.buffer)
            self.buff_type = wx.StaticText(self.buffer_low_panel, id=-1, label="File type: " + str(self.buffer))
            self.sub_2_sizer.Add(self.buff_type, 0, wx.LEFT | wx.ALIGN_CENTER_VERTICAL, 20)
            self.go_to = wx.BitmapButton(self.buffer_low_panel, id=-1, bitmap=wx.Bitmap(self.go_img), size=(30, 30),
                                         style=wx.BU_NOTEXT)
            self.go_to.SetLabel("https://1lib.in" + self.content_list[0]['href'])
            self.go_to.Bind(wx.EVT_BUTTON, self.on_click)
            self.sub_2_sizer.Add(self.go_to, 0, wx.LEFT, 20)

            self.buffer_panel_sizer.Add(self.buffer_low_panel, 0, flag=wx.TOP | wx.LEFT, border=5)
            self.node_list.append(self.buffer_low_panel)
            self.counter += 1


        self.buffer_panel.SetupScrolling()
        self.bottom_panel.Refresh()
        self.bottom_panel.Update()
        self.buffer_panel.Show()




class ArticlePanel(PanelBase):
    def __init__(self, parent, on_click):
        super(ArticlePanel, self).__init__(parent, 'ArticlePanel', on_click)


class PanelSwitcher(wx.BoxSizer):
    def __init__(self, parent, panels):
        wx.BoxSizer.__init__(self)
        parent.SetSizer(self)
        self.parent = parent
        self.panels = panels
        for panel in self.panels:
            self.Add(panel, 1, wx.EXPAND)

        self.panels[0].Show()

    def Show(self, panel):
        for p in self.panels:
            if p == panel:
                p.Show()
            else:
                p.Hide()
        self.parent.Layout()


class ShareFrame(wx.Frame):
    def __init__(self, title, parent=None):
        super(ShareFrame, self).__init__(parent=parent, title=title, style=wx.CAPTION|wx.CLOSE_BOX)
        self.SetBackgroundColour('#F8EDEB')
        self.SetId(wx.ID_ANY)
        self.SetSize(250, 400)
        self.def_image = wx.Image(r".\\Resources\\mominamustehsan.png")
        self.def_image = self.def_image.Rescale(width=84, height=114, quality=wx.IMAGE_QUALITY_HIGH)
        self.share_img = wx.Image(r".\\Resources\\icons\\share.png")
        self.share_img.Rescale(width=20, height=20, quality=wx.IMAGE_QUALITY_NORMAL)
        self.download_img = wx.Image(r".\\Resources\\icons\\download.png")
        self.download_img.Rescale(width=20, height=20, quality=wx.IMAGE_QUALITY_NORMAL)
        self.font1 = wx.Font(12, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Calibri')
        self.font2 = wx.Font(12, wx.MODERN, wx.BOLD, wx.NORMAL, False, u'Roboto')
        self.MainUI()
        self.Show()


    def MainUI(self):
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.main_sizer)

        self.top_panel = wx.Panel(self, id=-1, size=(250, 70), pos=(0, 0), style=wx.NO_BORDER)
        self.top_panel.SetBackgroundColour('#F8EDEB')
        self.middle_panel = wx.Panel(self, id=-1, size=(250, 145), pos=(0, 70), style=wx.SIMPLE_BORDER)
        self.middle_panel.SetBackgroundColour('#F8EDEB')
        self.bottom_panel = wx.Panel(self, id=-1, size=(250, 185), pos=(0, 215), style= wx.NO_BORDER)
        self.bottom_panel.SetBackgroundColour('#F8EDEB')

        self.main_sizer.Add(self.top_panel)
        self.main_sizer.Add(self.middle_panel)
        self.main_sizer.Add(self.bottom_panel, 0, wx.LEFT|wx.TOP, 5)

        self.top_main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.top_panel.SetSizer(self.top_main_sizer)
        self.middle_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.middle_panel.SetSizer(self.middle_sizer)
        self.bottom_sizer = wx.GridSizer(rows=7, cols=1, hgap=5, vgap=5)
        self.bottom_panel.SetSizer(self.bottom_sizer)

        # top panel
        self.book_name = wx.StaticText(self.top_panel, id=-1, label="--Book Name--",
                                       style=wx.ST_ELLIPSIZE_MIDDLE)
        self.book_name.SetFont(self.font2)
        self.top_main_sizer.Add(self.book_name, 0, flag=wx.TOP|wx.LEFT, border=20)

        # middle panel
        self.Book_bitmap = wx.BitmapButton(self.middle_panel, id=-1, size=(84, 114), bitmap=wx.Bitmap(self.def_image),
                                           style=wx.BU_NOTEXT)
        self.middle_sizer.Add(self.Book_bitmap, 0, flag=wx.LEFT | wx.TOP, border=20)

        self.screenshot = wx.BitmapButton(self.middle_panel, id=-1, size=(40, 40), style=wx.BU_LEFT)
        self.screenshot.Bind(wx.EVT_BUTTON, self.on_share)
        self.screenshot.SetLabel("Share")
        self.screenshot.SetBitmap(wx.Bitmap(self.share_img))

        self.download = wx.BitmapButton(self.middle_panel, id=-1, size=(40, 40), style=wx.BU_LEFT)
        self.download.SetLabel("download")
        self.download.SetBitmap(wx.Bitmap(self.download_img))


        self.middle_1_sizer = wx.BoxSizer(wx.VERTICAL)
        self.middle_sizer.Add(self.middle_1_sizer)

        self.middle_1_sizer.Add(self.screenshot, 0, flag=wx.TOP | wx.LEFT, border=25)
        self.middle_1_sizer.Add(self.download, 0, flag=wx.TOP | wx.LEFT, border=25)

        self.author = wx.StaticText(self.bottom_panel, id=-1, label="Author: --")
        self.author.SetFont(self.font1)
        self.isbn = wx.StaticText(self.bottom_panel, id=-1, label="ISBN: --")
        self.isbn.SetFont(self.font1)
        self.isbn_10 = wx.StaticText(self.bottom_panel, id=-1, label="ISBN 10: --")
        self.isbn_10.SetFont(self.font1)
        self.isbn_13 = wx.StaticText(self.bottom_panel, id=-1, label="ISBN 13: --")
        self.isbn_13.SetFont(self.font1)
        self.year = wx.StaticText(self.bottom_panel, id=-1, label="Year: --")
        self.year.SetFont(self.font1)
        self.file = wx.StaticText(self.bottom_panel, id=-1, label="File Type: --")
        self.file.SetFont(self.font1)

        self.bottom_sizer.Add(self.author)
        self.bottom_sizer.Add(self.isbn)
        self.bottom_sizer.Add(self.isbn_10)
        self.bottom_sizer.Add(self.isbn_13)
        self.bottom_sizer.Add(self.year)
        self.bottom_sizer.Add(self.file)

        self.scrape_detail("https://1lib.in/book/4971360/71472b?dsource=recommend")

    def on_share(self, event):
        self.Centre()

        hwnd = win32gui.FindWindow(None, "My Share Snorkeling")

        print(win32gui.GetWindowRect(hwnd))

        left, top, right, bottom = win32gui.GetWindowRect(hwnd)

        self.image = pyscreenshot.grab(bbox=(left, top, right, bottom))
        self.image.save("screenshot.png")



    def scrape_detail(self, arg):
        # init contents
        self.url_passed = arg

        # initialize scraping
        hdr = {'User-Agent': 'Mozilla/5.0'}
        request = Request(self.url_passed, headers=hdr)
        self.page_hex = urlopen(request)
        self.page_code = self.page_hex.read()
        self.page_hex.close()
        self.page_analytic = BeautifulSoup(self.page_code, features='html.parser')

        self.page_var = self.page_analytic.find('div', {"itemtype": "http://schema.org/Book"})
        self.b_details = self.page_var.find('div', {'class': "bookDetailsBox"})

        try:
            self.b_name = self.page_var.h1.get_text().strip()
            self.book_name.SetLabel(self.b_name)
        except AttributeError:
            pass

        # details
        try:
            self.b_auth = self.page_analytic.find('div', {'class': "col-sm-9"}).i.get_text()
            self.author.SetLabel("Author: "+self.b_auth)
        except AttributeError:
            pass

        try:
            self.b_isbn10 = self.b_details.find('div', {'class': "bookProperty property_isbn 10"}).find('div', {
                'class': "property_value"}).get_text()
            self.isbn_10.SetLabel("ISBN 10: "+self.b_isbn10)
        except AttributeError:
            pass

        try:
            self.b_isbn = self.b_details.find('div', {'class': "bookProperty property_isbn"}).find('div', {
                'class': "property_value"}).get_text()
            self.isbn.SetLabel("ISBN: "+self.b_isbn)
        except AttributeError:
            pass

        try:
            self.b_isbn13 = self.b_details.find('div', {'class': "bookProperty property_isbn 13"}).find('div', {
                'class': "property_value"}).get_text()
            self.isbn_13.SetLabel("ISBN 13:"+self.b_isbn13)
        except AttributeError:
            pass

        try:
            self.b_year = self.b_details.find('div', {'class': "bookProperty property_year"}).find('div', {
                'class': "property_value"}).get_text()
            self.year.SetLabel("Year: " + self.b_year)
        except AttributeError:
            pass

        self.b_type = self.b_details.find('div', {'class': "bookProperty property__file"}).find('div', {
            'class': "property_value"}).get_text()
        self.file.SetLabel("File Type: "+self.b_type)


        self.b_map = io.BytesIO(
            urlopen(Request(self.page_analytic.find('div', {'class': "col-sm-3"}).a.img['src'])).read())
        self.b_buffer = wx.Image(self.b_map).Rescale(width=84, height=114, quality=wx.IMAGE_QUALITY_NORMAL)

        self.Book_bitmap.SetBitmap(wx.Bitmap(self.b_buffer))

        self.top_panel.Update()
        self.middle_panel.Update()
        self.bottom_panel.Update()


class WindowFrame(wx.Frame):
    def __init__(self, parent=None):
        super(WindowFrame, self).__init__(parent, title='Z-library', style=wx.DEFAULT_FRAME_STYLE)
        self.SetSize((720, 480))
        self.Centre(direction=wx.BOTH)
        self.SetIcon(wx.Icon(r'.\\Resources\\Icons\\temperature.png'))

        # self.main_panel = MainPanel(self, self.on_main_panel_click)
        # self.logo_panel = LogoPanel(self, self.on_logo_panel_click)
        # self.d1_panel = DetailPanel1(self, self.on_d1_panel_click)
        # self.d2_panel = DetailPanel2(self, self.on_d2_panel_click)
        # self.article_panel = ArticlePanel(self, self.article_on_click)
        #
        # self.panel_switch = PanelSwitcher(self, [self.main_panel, self.logo_panel,
        #                                          self.d1_panel,self.d2_panel, self.article_panel])

        self.obj = ShareFrame("My Share Snorkeling", self)

        self.Menu_ui()


    def Menu_ui(self):
        self.menubar = wx.MenuBar(style=wx.MB_DOCKABLE)
        self.setting = wx.Menu()
        self.books_menu = wx.MenuItem(self.setting, id=-1, text="Books", kind=wx.ITEM_RADIO)
        self.article_menu = wx.MenuItem(self.setting, id=-1, text="Articles", kind=wx.ITEM_RADIO)
        self.setting.Append(self.books_menu)
        self.setting.Append(self.article_menu)
        self.setting.AppendSeparator()
        self.dark_theme = wx.MenuItem(self.setting, id=-1, text="Dark", kind=wx.ITEM_RADIO)
        self.light_theme = wx.MenuItem(self.setting, id=-1, text="Light", kind=wx.ITEM_RADIO)
        self.setting.Append(self.light_theme)
        self.setting.Append(self.dark_theme)
        self.setting.AppendSeparator()
        self.about_me = wx.MenuItem(self.setting, id=-1, text="About Me", kind=wx.ITEM_NORMAL)
        self.quit = wx.MenuItem(self.setting, id=-1, text="Quit", kind=wx.ITEM_NORMAL)
        self.setting.Append(self.about_me)
        self.setting.Append(self.quit)
        self.menubar.Append(self.setting, "Settings")
        self.SetMenuBar(self.menubar)

    # def on_main_panel_click(self, event):
    #     arg = event.GetEventObject().GetLabel()
    #     if "mostpopular" in arg:
    #         self.panel_switch.Hide(self.main_panel)
    #         self.panel_switch.Show(self.d1_panel)
    #         self.d1_panel.scrape_detail(arg)
    #     else:
    #         print("Here")
    #         arg = event.GetEventObject().GetValue()
    #         arg = "https://1lib.in/s/" + arg
    #         print("Url_accessing: " + arg)
    #         self.panel_switch.Hide(self.d1_panel)
    #         self.d2_panel.list_scrape(arg)
    #         self.panel_switch.Show(self.d2_panel)
    #
    # def on_logo_panel_click(self):
    #     pass
    #
    # def on_d1_panel_click(self, event):
    #     if "mostpopular" in event.GetEventObject().GetLabel():
    #         self.panel_switch.Hide(self.d1_panel)
    #         self.d1_panel.scrape_detail(event.GetEventObject().GetLabel())
    #         self.panel_switch.Show(self.d1_panel)
    #     else:
    #         pass
    #
    # def on_d2_panel_click(self, event):
    #     self.args = event.GetEventObject().GetLabel()
    #     self.obj.scrape_detail(self.args)
    #     self.obj.Show()
    #
    # def article_on_click(self):
    #     pass
    #
    # def on_detail_click(self, event):
    #     pass




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app_obj = wx.App(redirect=False)
    app_obj.locale = wx.Locale(wx.LANGUAGE_ENGLISH)
    frame_obj = WindowFrame()
    frame_obj.Show()
    app_obj.MainLoop()

