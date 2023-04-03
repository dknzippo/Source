# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 3.10.0-4761b0c)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class Main
###########################################################################

class Main ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Material Checker Prototype v0.4 (+Pants)", pos = wx.DefaultPosition, size = wx.Size( 1859,1159 ), style = wx.CAPTION|wx.CLOSE_BOX|wx.MAXIMIZE|wx.MAXIMIZE_BOX|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		fgSizer1 = wx.FlexGridSizer( 1, 1, 0, 0 )
		fgSizer1.AddGrowableCol( 0 )
		fgSizer1.AddGrowableRow( 0 )
		fgSizer1.SetFlexibleDirection( wx.BOTH )
		fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_ALL )

		fgSizer3 = wx.FlexGridSizer( 0, 1, 10, 10 )
		fgSizer3.AddGrowableCol( 0 )
		fgSizer3.AddGrowableRow( 0 )
		fgSizer3.SetFlexibleDirection( wx.BOTH )
		fgSizer3.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_ALL )

		gSizer8 = wx.GridSizer( 0, 3, 5, 5 )

		sbSizer5 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Material ID's" ), wx.VERTICAL )

		gSizer4 = wx.GridSizer( 0, 1, 0, 0 )

		m_listBox_DecoIDChoices = []
		self.m_listBox_DecoID = wx.ListBox( sbSizer5.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_listBox_DecoIDChoices, wx.LB_NEEDED_SB|wx.BORDER_NONE )
		self.m_listBox_DecoID.SetFont( wx.Font( 40, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
		self.m_listBox_DecoID.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_APPWORKSPACE ) )

		gSizer4.Add( self.m_listBox_DecoID, 0, wx.EXPAND, 5 )


		sbSizer5.Add( gSizer4, 1, wx.EXPAND, 5 )


		gSizer8.Add( sbSizer5, 1, wx.EXPAND, 5 )

		sbSizer8 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Color && Barcode Status" ), wx.VERTICAL )

		gSizer5 = wx.GridSizer( 0, 1, 0, 0 )

		bSizer5 = wx.BoxSizer( wx.VERTICAL )

		gSizer41 = wx.GridSizer( 0, 2, 0, 0 )

		self.m_staticText_BarcodeID1 = wx.StaticText( sbSizer8.GetStaticBox(), wx.ID_ANY, u"Color:", wx.DefaultPosition, wx.Size( 200,-1 ), wx.ALIGN_LEFT )
		self.m_staticText_BarcodeID1.Wrap( -1 )

		self.m_staticText_BarcodeID1.SetFont( wx.Font( 50, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

		gSizer41.Add( self.m_staticText_BarcodeID1, 0, wx.ALL, 5 )

		self.m_staticText_ColorID = wx.StaticText( sbSizer8.GetStaticBox(), wx.ID_ANY, u"--", wx.DefaultPosition, wx.Size( 200,-1 ), wx.ALIGN_RIGHT )
		self.m_staticText_ColorID.Wrap( -1 )

		self.m_staticText_ColorID.SetFont( wx.Font( 50, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

		gSizer41.Add( self.m_staticText_ColorID, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )


		bSizer5.Add( gSizer41, 1, wx.EXPAND, 5 )

		self.m_panelColor = wx.Panel( sbSizer8.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer5.Add( self.m_panelColor, 1, wx.EXPAND |wx.ALL, 5 )


		gSizer5.Add( bSizer5, 1, wx.EXPAND, 5 )

		bSizer6 = wx.BoxSizer( wx.VERTICAL )

		gSizer51 = wx.GridSizer( 0, 2, 0, 0 )

		self.m_staticText11 = wx.StaticText( sbSizer8.GetStaticBox(), wx.ID_ANY, u"Barcode:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText11.Wrap( -1 )

		self.m_staticText11.SetFont( wx.Font( 50, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

		gSizer51.Add( self.m_staticText11, 0, wx.ALL, 5 )

		self.m_staticText_BarcodeID = wx.StaticText( sbSizer8.GetStaticBox(), wx.ID_ANY, u"--", wx.DefaultPosition, wx.Size( 200,-1 ), wx.ALIGN_RIGHT )
		self.m_staticText_BarcodeID.Wrap( -1 )

		self.m_staticText_BarcodeID.SetFont( wx.Font( 50, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

		gSizer51.Add( self.m_staticText_BarcodeID, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )

		self.m_staticText111 = wx.StaticText( sbSizer8.GetStaticBox(), wx.ID_ANY, u"System:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText111.Wrap( -1 )

		self.m_staticText111.SetFont( wx.Font( 20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

		gSizer51.Add( self.m_staticText111, 0, wx.ALL, 5 )

		self.m_staticText_SystemID = wx.StaticText( sbSizer8.GetStaticBox(), wx.ID_ANY, u"--", wx.DefaultPosition, wx.Size( 200,-1 ), wx.ALIGN_RIGHT )
		self.m_staticText_SystemID.Wrap( -1 )

		self.m_staticText_SystemID.SetFont( wx.Font( 20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

		gSizer51.Add( self.m_staticText_SystemID, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )


		bSizer6.Add( gSizer51, 1, wx.EXPAND, 5 )

		bSizer2 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticTextColorBar1 = wx.StaticText( sbSizer8.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL|wx.ST_NO_AUTORESIZE )
		self.m_staticTextColorBar1.Wrap( -1 )

		self.m_staticTextColorBar1.SetFont( wx.Font( 30, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

		bSizer2.Add( self.m_staticTextColorBar1, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_staticTextColorBar2 = wx.StaticText( sbSizer8.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL|wx.ST_NO_AUTORESIZE )
		self.m_staticTextColorBar2.Wrap( -1 )

		self.m_staticTextColorBar2.SetFont( wx.Font( 30, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

		bSizer2.Add( self.m_staticTextColorBar2, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_staticTextColorBar3 = wx.StaticText( sbSizer8.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL|wx.ST_NO_AUTORESIZE )
		self.m_staticTextColorBar3.Wrap( -1 )

		self.m_staticTextColorBar3.SetFont( wx.Font( 30, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

		bSizer2.Add( self.m_staticTextColorBar3, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_staticTextColorBar4 = wx.StaticText( sbSizer8.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL|wx.ST_NO_AUTORESIZE )
		self.m_staticTextColorBar4.Wrap( -1 )

		self.m_staticTextColorBar4.SetFont( wx.Font( 30, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

		bSizer2.Add( self.m_staticTextColorBar4, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_staticTextColorBar5 = wx.StaticText( sbSizer8.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL|wx.ST_NO_AUTORESIZE )
		self.m_staticTextColorBar5.Wrap( -1 )

		self.m_staticTextColorBar5.SetFont( wx.Font( 30, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
		self.m_staticTextColorBar5.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_APPWORKSPACE ) )

		bSizer2.Add( self.m_staticTextColorBar5, 0, wx.ALL|wx.EXPAND, 5 )


		bSizer6.Add( bSizer2, 1, wx.EXPAND, 5 )


		gSizer5.Add( bSizer6, 1, wx.EXPAND, 5 )


		sbSizer8.Add( gSizer5, 1, wx.EXPAND, 5 )


		gSizer8.Add( sbSizer8, 1, wx.EXPAND, 5 )

		sbSizer52 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, wx.EmptyString ), wx.VERTICAL )

		fgSizer31 = wx.FlexGridSizer( 2, 1, 0, 0 )
		fgSizer31.AddGrowableRow( 1 )
		fgSizer31.SetFlexibleDirection( wx.BOTH )
		fgSizer31.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		sbSizer511 = wx.StaticBoxSizer( wx.StaticBox( sbSizer52.GetStaticBox(), wx.ID_ANY, u"Figure Connection" ), wx.VERTICAL )

		fgSizer4 = wx.FlexGridSizer( 3, 1, 0, 0 )
		fgSizer4.SetFlexibleDirection( wx.BOTH )
		fgSizer4.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		gSizer6 = wx.GridSizer( 0, 3, 0, 0 )

		self.m_radioBtn_ble = wx.RadioButton( sbSizer511.GetStaticBox(), wx.ID_ANY, u"BLE", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_radioBtn_ble.SetValue( True )
		self.m_radioBtn_ble.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNTEXT ) )
		self.m_radioBtn_ble.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_APPWORKSPACE ) )

		gSizer6.Add( self.m_radioBtn_ble, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		m_choice_figure_macChoices = []
		self.m_choice_figure_mac = wx.Choice( sbSizer511.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_figure_macChoices, 0 )
		self.m_choice_figure_mac.SetSelection( 0 )
		self.m_choice_figure_mac.Enable( False )

		gSizer6.Add( self.m_choice_figure_mac, 0, wx.ALL|wx.EXPAND, 5 )

		gSizer7 = wx.GridSizer( 0, 2, 0, 0 )

		self.m_button_RefreshBLE = wx.Button( sbSizer511.GetStaticBox(), wx.ID_ANY, u"Scan...", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_button_RefreshBLE.Enable( False )

		gSizer7.Add( self.m_button_RefreshBLE, 0, wx.ALL, 5 )

		gSizer81 = wx.GridSizer( 2, 1, 0, 0 )

		self.m_checkBoxFilter = wx.CheckBox( sbSizer511.GetStaticBox(), wx.ID_ANY, u"Filter LEGO", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_checkBoxFilter.SetValue(True)
		self.m_checkBoxFilter.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNTEXT ) )
		self.m_checkBoxFilter.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_APPWORKSPACE ) )

		gSizer81.Add( self.m_checkBoxFilter, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		self.m_checkBoxRandomMac = wx.CheckBox( sbSizer511.GetStaticBox(), wx.ID_ANY, u"Random Adr", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_checkBoxRandomMac.SetValue(True)
		self.m_checkBoxRandomMac.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNTEXT ) )
		self.m_checkBoxRandomMac.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_APPWORKSPACE ) )

		gSizer81.Add( self.m_checkBoxRandomMac, 0, wx.ALL, 5 )


		gSizer7.Add( gSizer81, 1, wx.EXPAND, 5 )


		gSizer6.Add( gSizer7, 1, wx.EXPAND, 5 )


		fgSizer4.Add( gSizer6, 1, wx.EXPAND, 5 )

		gSizer10 = wx.GridSizer( 1, 3, 0, 0 )

		self.m_radioBtn_utm = wx.RadioButton( sbSizer511.GetStaticBox(), wx.ID_ANY, u"UART", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_radioBtn_utm.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNTEXT ) )
		self.m_radioBtn_utm.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_APPWORKSPACE ) )

		gSizer10.Add( self.m_radioBtn_utm, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		m_choice_comport_utmChoices = []
		self.m_choice_comport_utm = wx.Choice( sbSizer511.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice_comport_utmChoices, 0 )
		self.m_choice_comport_utm.SetSelection( 0 )
		self.m_choice_comport_utm.Enable( False )

		gSizer10.Add( self.m_choice_comport_utm, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_button_RefreshComMac = wx.Button( sbSizer511.GetStaticBox(), wx.ID_ANY, u"Refresh", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_button_RefreshComMac.Enable( False )

		gSizer10.Add( self.m_button_RefreshComMac, 0, wx.ALL, 5 )


		fgSizer4.Add( gSizer10, 1, wx.EXPAND, 5 )

		gSizer11 = wx.GridSizer( 0, 5, 0, 0 )

		self.m_button_FigureConnect = wx.Button( sbSizer511.GetStaticBox(), wx.ID_ANY, u"Connect", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_button_FigureConnect.Enable( False )

		gSizer11.Add( self.m_button_FigureConnect, 0, wx.ALL, 5 )

		self.m_button_FigureDisconnect = wx.Button( sbSizer511.GetStaticBox(), wx.ID_ANY, u"Disconnect", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_button_FigureDisconnect.Enable( False )

		gSizer11.Add( self.m_button_FigureDisconnect, 0, wx.ALL, 5 )


		fgSizer4.Add( gSizer11, 1, wx.EXPAND, 5 )


		sbSizer511.Add( fgSizer4, 1, wx.EXPAND, 5 )


		fgSizer31.Add( sbSizer511, 1, wx.EXPAND, 5 )

		sbSizer51 = wx.StaticBoxSizer( wx.StaticBox( sbSizer52.GetStaticBox(), wx.ID_ANY, u"Information" ), wx.VERTICAL )

		self.m_staticText39 = wx.StaticText( sbSizer51.GetStaticBox(), wx.ID_ANY, u"This program may only be used for checking if material id's match actual production.\n", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText39.Wrap( -1 )

		self.m_staticText39.SetFont( wx.Font( 15, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

		sbSizer51.Add( self.m_staticText39, 0, wx.ALL|wx.EXPAND, 5 )

		fgSizer5 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer5.AddGrowableCol( 1 )
		fgSizer5.SetFlexibleDirection( wx.BOTH )
		fgSizer5.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText14 = wx.StaticText( sbSizer51.GetStaticBox(), wx.ID_ANY, u"Figure FW:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText14.Wrap( -1 )

		fgSizer5.Add( self.m_staticText14, 0, wx.ALL, 5 )

		self.m_staticTextFigureFW = wx.StaticText( sbSizer51.GetStaticBox(), wx.ID_ANY, u"n/a", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticTextFigureFW.Wrap( -1 )

		fgSizer5.Add( self.m_staticTextFigureFW, 0, wx.ALL, 5 )

		self.m_staticText17 = wx.StaticText( sbSizer51.GetStaticBox(), wx.ID_ANY, u"Figure HW:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText17.Wrap( -1 )

		fgSizer5.Add( self.m_staticText17, 0, wx.ALL, 5 )

		self.m_staticTextFigureHW = wx.StaticText( sbSizer51.GetStaticBox(), wx.ID_ANY, u"n/a", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticTextFigureHW.Wrap( -1 )

		fgSizer5.Add( self.m_staticTextFigureHW, 0, wx.ALL, 5 )

		self.m_staticText19 = wx.StaticText( sbSizer51.GetStaticBox(), wx.ID_ANY, u"material_list.json modified:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText19.Wrap( -1 )

		fgSizer5.Add( self.m_staticText19, 0, wx.ALL, 5 )

		self.m_staticTextJsonTimestamp = wx.StaticText( sbSizer51.GetStaticBox(), wx.ID_ANY, u"n/a", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticTextJsonTimestamp.Wrap( -1 )

		fgSizer5.Add( self.m_staticTextJsonTimestamp, 0, wx.ALL, 5 )

		self.m_staticText21 = wx.StaticText( sbSizer51.GetStaticBox(), wx.ID_ANY, u"material_list.json items:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText21.Wrap( -1 )

		fgSizer5.Add( self.m_staticText21, 0, wx.ALL, 5 )

		self.m_staticTextJsonItems = wx.StaticText( sbSizer51.GetStaticBox(), wx.ID_ANY, u"n/a", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticTextJsonItems.Wrap( -1 )

		fgSizer5.Add( self.m_staticTextJsonItems, 0, wx.ALL, 5 )

		self.m_staticText211 = wx.StaticText( sbSizer51.GetStaticBox(), wx.ID_ANY, u"Pants:", wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		self.m_staticText211.Wrap( -1 )

		self.m_staticText211.SetFont( wx.Font( 20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

		fgSizer5.Add( self.m_staticText211, 0, wx.ALL, 5 )

		fgSizer6 = wx.FlexGridSizer( 1, 6, 0, 0 )
		fgSizer6.SetFlexibleDirection( wx.BOTH )
		fgSizer6.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticTextPants1 = wx.StaticText( sbSizer51.GetStaticBox(), wx.ID_ANY, u"1", wx.DefaultPosition, wx.Size( 50,50 ), wx.ALIGN_CENTER_HORIZONTAL|wx.ST_NO_AUTORESIZE|wx.BORDER_SIMPLE )
		self.m_staticTextPants1.Wrap( -1 )

		self.m_staticTextPants1.SetFont( wx.Font( 30, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

		fgSizer6.Add( self.m_staticTextPants1, 0, wx.ALL, 5 )

		self.m_staticTextPants2 = wx.StaticText( sbSizer51.GetStaticBox(), wx.ID_ANY, u"2", wx.DefaultPosition, wx.Size( 50,50 ), wx.ALIGN_CENTER_HORIZONTAL|wx.ST_NO_AUTORESIZE|wx.BORDER_SIMPLE )
		self.m_staticTextPants2.Wrap( -1 )

		self.m_staticTextPants2.SetFont( wx.Font( 30, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

		fgSizer6.Add( self.m_staticTextPants2, 0, wx.ALL, 5 )

		self.m_staticTextPants3 = wx.StaticText( sbSizer51.GetStaticBox(), wx.ID_ANY, u"3", wx.DefaultPosition, wx.Size( 50,50 ), wx.ALIGN_CENTER_HORIZONTAL|wx.ST_NO_AUTORESIZE|wx.BORDER_SIMPLE )
		self.m_staticTextPants3.Wrap( -1 )

		self.m_staticTextPants3.SetFont( wx.Font( 30, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

		fgSizer6.Add( self.m_staticTextPants3, 0, wx.ALL, 5 )

		self.m_staticTextPants4 = wx.StaticText( sbSizer51.GetStaticBox(), wx.ID_ANY, u"4", wx.DefaultPosition, wx.Size( 50,50 ), wx.ALIGN_CENTER_HORIZONTAL|wx.ST_NO_AUTORESIZE|wx.BORDER_SIMPLE )
		self.m_staticTextPants4.Wrap( -1 )

		self.m_staticTextPants4.SetFont( wx.Font( 30, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

		fgSizer6.Add( self.m_staticTextPants4, 0, wx.ALL, 5 )

		self.m_staticTextPants5 = wx.StaticText( sbSizer51.GetStaticBox(), wx.ID_ANY, u"5", wx.DefaultPosition, wx.Size( 50,50 ), wx.ALIGN_CENTER_HORIZONTAL|wx.ST_NO_AUTORESIZE|wx.BORDER_SIMPLE )
		self.m_staticTextPants5.Wrap( -1 )

		self.m_staticTextPants5.SetFont( wx.Font( 30, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

		fgSizer6.Add( self.m_staticTextPants5, 0, wx.ALL, 5 )

		self.m_staticTextPants6 = wx.StaticText( sbSizer51.GetStaticBox(), wx.ID_ANY, u"6", wx.DefaultPosition, wx.Size( 50,50 ), wx.ALIGN_CENTER_HORIZONTAL|wx.ST_NO_AUTORESIZE|wx.BORDER_SIMPLE )
		self.m_staticTextPants6.Wrap( -1 )

		self.m_staticTextPants6.SetFont( wx.Font( 30, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

		fgSizer6.Add( self.m_staticTextPants6, 0, wx.ALL, 5 )


		fgSizer5.Add( fgSizer6, 1, wx.ALL|wx.EXPAND, 5 )


		sbSizer51.Add( fgSizer5, 1, wx.EXPAND, 5 )


		fgSizer31.Add( sbSizer51, 1, wx.ALL|wx.EXPAND, 5 )


		sbSizer52.Add( fgSizer31, 1, wx.EXPAND, 5 )


		gSizer8.Add( sbSizer52, 1, wx.EXPAND, 5 )


		fgSizer3.Add( gSizer8, 1, wx.ALL|wx.EXPAND, 5 )


		fgSizer1.Add( fgSizer3, 1, wx.ALL|wx.EXPAND, 5 )


		self.SetSizer( fgSizer1 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.Bind( wx.EVT_CLOSE, self.OnClose )
		self.m_radioBtn_ble.Bind( wx.EVT_RADIOBUTTON, self.UpdateFigureConnectionselection )
		self.m_button_RefreshBLE.Bind( wx.EVT_BUTTON, self.OnClickRefreshBLE )
		self.m_radioBtn_utm.Bind( wx.EVT_RADIOBUTTON, self.UpdateFigureConnectionselection )
		self.m_button_RefreshComMac.Bind( wx.EVT_BUTTON, self.OnClickRefreshComMac )
		self.m_button_FigureConnect.Bind( wx.EVT_BUTTON, self.OnClickFigureConnect )
		self.m_button_FigureDisconnect.Bind( wx.EVT_BUTTON, self.OnClickFigureDisconnect )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def OnClose( self, event ):
		event.Skip()

	def UpdateFigureConnectionselection( self, event ):
		event.Skip()

	def OnClickRefreshBLE( self, event ):
		event.Skip()


	def OnClickRefreshComMac( self, event ):
		event.Skip()

	def OnClickFigureConnect( self, event ):
		event.Skip()

	def OnClickFigureDisconnect( self, event ):
		event.Skip()


