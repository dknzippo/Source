# -*- coding: cp1252 -*-
import gui
import wx
import os
from datetime import datetime, date
import time
from lble_extractors import *
from lble_inserters import *
import threading
from binascii import hexlify
import array
import pygatt
from serial.tools import list_ports
import serial
import time
import numpy as np
import json
import binascii
import os.path

_messages = {
             'HubProperties': 0x01
           ,'HubActions': 0x02
           ,'HubAlerts': 0x03
           ,'HubAttachedIO': 0x04
           ,'ErrorMessages': 0x05
           ,'EnterBootloaderMode': 0x10
           ,'LockMemory': 0x11
           ,'PortInformationRequest': 0x21
           ,'PortModeInformationRequest': 0x22
           ,'PortInputFormatSetupSingle': 0x41
           ,'PortInputFormatSetupCombined': 0x42
           ,'PortInformation': 0x43
           ,'PortModeInformation': 0x44
           ,'PortValueSingle': 0x45
           ,'PortValueCombined': 0x46
           ,'PortInputFormatSingle': 0x47
           ,'PortInputFormatCombined': 0x48
           ,'VirtualPortSetup': 0x61
           ,'PortOutputCommand': 0x81
           ,'PortOutputCommandFeedback': 0x82
        }

#inherit from the MainFrame created in wxFowmBuilder
class MainFrame(gui.Main):

    _barcode = 0
    
    _barcodeId = 0
    _colorId = 0
    _newTagDataReady = False
    _newPantsDataReady = False
    _olddecodeType = 0
    _decodeType = 0
    _olddecodeValue = 0
    _decodeValue = 0
    _rawBarcodeId = 0
    _rawColorId = 0
    _oldRawColor = 0
    _oldRawBarcodeId = 0
    BarcodeChangeCounter = 0
    _measurePixartHeaderLength = False
    _PixartHeaderLength = 0
    ser = None
    _DatabaseID = 0

    _pants = 0

    adapter = None
    _bleReady = False
    _utmReady = False

    _fw = 'n/a'
    _hw = 'n/a'
    
    #constructor
    def __init__(self,parent):

        #initialize parent class
        gui.Main.__init__(self,parent)

        # Try to open material json (must be UTF8 - no BOM)
        try:
            with open('material_list.json') as json_file:
                self.jsonMaterialData = json.load(json_file)  
        except Exception:
            print('"material_list.json" could not be found or it contains errors! Verify that encoding is UTF8 no BOM.')
            wx.MessageBox('"material_list.json" could not be found or it contains errors! Verify that encoding is UTF8 no BOM.', 'material_list.json missing', wx.OK | wx.ICON_ERROR)
            self.Destroy()
            return

        # This is not very good. But when using exepacker the OnShow event is never called, so instead we wait and hope that all controls are initialized before using them
        time.sleep(2)

        # Update info about json file. We do not have a header in the data, so show timestamp of file and items
        materialCount = 0
        for dict in self.jsonMaterialData['Material array']:
            materialCount = materialCount + 1
            
        self.m_staticTextJsonTimestamp.SetLabel(time.ctime(os.path.getmtime('material_list.json')))
        self.m_staticTextJsonItems.SetLabel(str(materialCount))
        

        self.RefreshComports()
        
        self.UpdateFigureConnectionselection()
        
        #self.connectWTM(port='COM16', handledCallback=self.Callback)
        
    def OnClose(self,event):
        
        self.disconnectUTM()
        
        self.Destroy()
        
       
    def RefreshComports(self):

        # List available figures MAC
        self.m_choice_comport_utm.Clear()
        
        try:
            ports = []
            for port, desc, hwid in sorted(list_ports.comports()):
                ports.append(port)
            self.m_choice_comport_utm.SetItems(ports)

            if len(ports) > 0:
                self.m_choice_comport_utm.SetSelection(0)
                
        except Exception:
            print('error')

    def connectWTM(self, port, handledCallback = None):

        try:
            # configure the serial connection
            self.ser = serial.Serial(
                port=port,
                baudrate=115200,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=None
            )
        except Exception:
            print('Could not connect to test box!\nVerify that cable connection and comport is correct.\nTry to reinsert USB cable and restart program.')
            return


        if self.ser.isOpen():
            self._utmReady = True

            self.thread = threading.Thread(target=self.WTMreceiveData, args=(self.ser,))
            self.thread.start()

            time.sleep(0.1)

            self._mac = None

            retryCount = 3
            
            while self._mac == None and retryCount > 0:

                print("Connecting WTM...")

                # Enter WTM mode  
                b = [0x0A, 0x00, 0x14, 0x4C, 0x45, 0x47, 0x4F, 0x2D, 0x50, 0x54]
                self.ser.write(str(bytearray(b)))

                time.sleep(0.1)

                # Try to read back mac

                print("Reading MAC...")
                b = [0x05, 0x00, 0x01, 0x0D, 0x05]
                self.ser.write(str(bytearray(b)))

                time.sleep(0.1)

                if self._mac == None:
                    retryCount = retryCount-1
                    print("Figure not responding! Retry command in 5 seconds...Close program and reinsert USB cable if error continunes.")
                    time.sleep(5)
                
                # Try to read back fw
                self._fw = None
                while self._fw == None and retryCount > 0:
                    print("Reading FW...")
                    b = [0x05, 0x00, 0x01, 0x03, 0x05]
                    self.ser.write(str(bytearray(b)))
                    time.sleep(0.1)
                    if self._fw == None:
                        retryCount = retryCount-1
                        print("Figure not responding! Retry command in 5 seconds...")
                        time.sleep(5)

                self._hw = None
                # Try to read back hw
                while self._hw == None and retryCount > 0:
                    print("Reading HW...")
                    b = [0x05, 0x00, 0x01, 0x04, 0x05]
                    self.ser.write(str(bytearray(b)))
                    time.sleep(0.1)
                    if self._hw == None:
                        retryCount = retryCount-1
                        print("Figure not responding! Retry command in 5 seconds...")
                        time.sleep(5)
                        
                
                        
            if retryCount == 0:
                wx.MessageBox('Check if correct com port is selected.\r\nClose program and reinsert USB cable if error continunes.', 'Figure not responding', wx.OK | wx.ICON_ERROR)
                self.ser.close()
                #self.disconnectUTM()
                return

            print('WTM connected to ' + self._mac)
            print('FW: ' + self._fw)
            print('HW: ' + self._hw)
            
            time.sleep(0.1)
            
            # Enter pixart logmode
            b = [0x05, 0x00, 0x15, 0x0D, 0x01]
            self.ser.write(str(bytearray(b)))

            # Read Pixart header length to support different firmware versions
            self._measurePixartHeaderLength = True
            # Wait for result
            while self._measurePixartHeaderLength:
                pass

            if self._PixartHeaderLength == 18:
                print("Figure identified to be running NEW FW with extended output")
            elif self._PixartHeaderLength == 15:
                print("Figure identified to be running OLD FW with minimum output")
            elif self._PixartHeaderLength == 17:
                print("Figure identified to be running NEW FW with dual header output")
            elif self._PixartHeaderLength == 22:
                print("Figure identified to be running NEW FW with triple header output  + checksum")
            else:
                print("Figure identified to be running unknown FW with Pixart datalength=" + str(self._PixartHeaderLength))

            print("Keep this window running and only exit program from interface window!")


            
        return self.ser.isOpen()
    
        
    def WTMreceiveData(self, ser):
        while ser.isOpen() and self._utmReady:
            # Wait for full header
            
            # Header 0xAA55 - int16
            # dataStatus - uint8
            # colorID - uint16
            # barcode - uint16
            # frameCnt - uint16
            # Ravg - uint8
            # Gavg - uint8
            # Bavg - uint8

                  #uint8_t OTPPassBit;
                  #uint8_t ModuleID;
                  #uint8_t AmbientSync;
                  #uint8_t IntensitySync;
                  #uint8_t AEState;
            
            # colorIDConverted - uint16
            # TagNo - uint8


            # Waiting for command header and synchronize communication
            while (True):
                cmd1 = ord(ser.read(1))
                if cmd1==0x0D or cmd1 == 0xAA or cmd1 == 0x03 or cmd1 == 0x04:
                    cmd2 = ord(ser.read(1))
                        
                    if cmd2==0x06 or cmd2 == 0x55:
                        break

            # Found header for MAC reply
            if(cmd1 == 0x0D and cmd2 == 0x06):
                # wait for all data
                while (ser.inWaiting() < 6 and ser.inWaiting() != 0):
                    pass
                        
                # Clean array
                m = None
                m = array.array('B',)
                # Fill array
                for index in range(6):
                    m.append(ord(ser.read(1)))

                macstring = hexlify(m)
                self._mac = '.'.join(a+b for a,b in zip(macstring[::2], macstring[1::2]))

            # Found header for FW reply
            if(cmd1 == 0x03 and cmd2 == 0x06):

                # wait for all data
                while (ser.inWaiting() < 4 and ser.inWaiting() != 0):
                    pass
                        
                # Clean array
                m = None
                m = array.array('B',)
                # Fill array
                for index in range(4):
                    #m.append(ord(ser.read(1)))
                    m.insert(0, ord(ser.read(1))) # reverse string according to hw byte format

                macstring = hexlify(m)
                self._fw = '.'.join(a+b for a,b in zip(macstring[::2], macstring[1::2]))

            # Found header for HW reply
            if(cmd1 == 0x04 and cmd2 == 0x06):
                # wait for all data
                while (ser.inWaiting() < 4):
                    pass
                        
                # Clean array
                m = None
                m = array.array('B',)
                # Fill array
                for index in range(4):
                    #m.append(ord(ser.read(1)))
                    m.insert(0, ord(ser.read(1))) # reverse string according to hw byte format

                macstring = hexlify(m)
                self._hw = '.'.join(a+b for a,b in zip(macstring[::2], macstring[1::2]))
                

            # Found header for Pixart data
            if(cmd1 == 0xAA and cmd2 == 0x55):

                # Count chars between 2 headers to identify FW on figure
                if self._measurePixartHeaderLength:
                    
                    self._PixartHeaderLength = 0
                    
                    while (True):
                        self._PixartHeaderLength = self._PixartHeaderLength + 1
                        if ord(ser.read(1)) == 0xAA:
                            if ord(ser.read(1)) == 0x55:
                                break
                            
                        if self._PixartHeaderLength > 30:
                            print("error _PixartHeaderLength")
                            ser.read(1)
                            self._PixartHeaderLength = 0
                            
                    self._PixartHeaderLength = self._PixartHeaderLength - 2
                    self._measurePixartHeaderLength = False

                else:

                    # Clean array
                    m = None
                    m = array.array('B',)
                       
                    # wait for all data
                    while (ser.inWaiting() < self._PixartHeaderLength):
                        pass

                    # Fill array
                    for index in range(self._PixartHeaderLength+1):
                        m.append(ord(ser.read(1)))
                            
                    
                    self._oldcolorId = self._colorId
                    self._oldbarcode = self._barcodeId

                    self._olddecodeType = self._decodeType
                    self._olddecodeValue = self._decodeValue

                    self._oldRawColor = self._rawColorId;
                    self._oldRawBarcodeId = self._rawBarcodeId;
                    
                        
                    # Parse array
                    # Read dataStatus
                    _dataStatus = np.uint8(ExtractInt8(m, {'offset': (0 * 1)}))

                    # Read unconverted color id
                    _colorIDlsb = np.uint8(ExtractInt8(m, {'offset': (1 * 1)}))
                    _colorIDmsb = np.uint8(ExtractInt8(m, {'offset': (2 * 1)}))

                    #self._confidenceRGB = (self._confidenceRGBmsb << 8) | self._confidenceRGBlsb
                    self._rawColorId = (_colorIDlsb & 0xFF)
                    self._rawColorId += (_colorIDmsb << 8)

                    _rawBarcodeIDlsb = np.uint8(ExtractInt8(m, {'offset': (3 * 1)}))
                    _rawBarcodeIDmsb = np.uint8(ExtractInt8(m, {'offset': (4 * 1)}))
                    
                    self._rawBarcodeId = (_rawBarcodeIDlsb & 0xFF)
                    self._rawBarcodeId += (_rawBarcodeIDmsb << 8)
                    
                    # Framecount 16 bit

                    # confidence ?
                    
                    self._R = np.uint8(ExtractInt8(m, {'offset': (7 * 1)}))
                    self._G = np.uint8(ExtractInt8(m, {'offset': (8 * 1)}))
                    self._B = np.uint8(ExtractInt8(m, {'offset': (9 * 1)}))


                    # New FW with extended output
                    if self._PixartHeaderLength == 18:
                            
                        # New header
                        self._OTPPassBit = np.uint8(ExtractInt8(m, {'offset': (10 * 1)}))
                        self._ModuleID = np.uint8(ExtractInt8(m, {'offset': (11 * 1)}))
                        self._AmbientSync = np.uint8(ExtractInt8(m, {'offset': (12 * 1)}))
                        self._IntensitySync = np.uint8(ExtractInt8(m, {'offset': (13 * 1)}))
                        self._AEState = np.uint8(ExtractInt8(m, {'offset': (14 * 1)}))
                                            

                        # Read converted color id
                        _colorIDlsb = np.uint8(ExtractInt8(m, {'offset': (15 * 1)}))
                        _colorIDmsb = np.uint8(ExtractInt8(m, {'offset': (16 * 1)}))
                        self._colorId = (_colorIDlsb & 0xFF)
                        self._colorId += (_colorIDmsb << 8)

                        # Barcode TagNR
                        self._barcodeId = np.uint8(ExtractInt8(m, {'offset': (17 * 1)}))


                    # New optimized header with support for 2 databases
                    elif self._PixartHeaderLength == 17 or self._PixartHeaderLength == 22:

                        _dataStatus = np.uint8(ExtractInt8(m, {'offset': (0 * 1)}))
                        
                        # Read unconverted color id
                        _colorIDlsb = np.uint8(ExtractInt8(m, {'offset': (1 * 1)}))
                        _colorIDmsb = np.uint8(ExtractInt8(m, {'offset': (2 * 1)}))
                        self._rawColorId = (_colorIDlsb & 0xFF)
                        self._rawColorId += (_colorIDmsb << 8)


                        _rawBarcodeIDlsb = np.uint8(ExtractInt8(m, {'offset': (3 * 1)}))
                        _rawBarcodeIDmsb = np.uint8(ExtractInt8(m, {'offset': (4 * 1)}))
                        self._rawBarcodeId = (_rawBarcodeIDlsb & 0xFF)
                        self._rawBarcodeId += (_rawBarcodeIDmsb << 8)

                        _frameCntlsb = np.uint8(ExtractInt8(m, {'offset': (5 * 1)}))
                        _frameCntmsb = np.uint8(ExtractInt8(m, {'offset': (6 * 1)}))
                        self._frameCnt = (_frameCntlsb & 0xFF)
                        self._frameCnt += (_frameCntmsb << 8)
                        
                        self._R = np.uint8(ExtractInt8(m, {'offset': (7 * 1)}))
                        self._G = np.uint8(ExtractInt8(m, {'offset': (8 * 1)}))
                        self._B = np.uint8(ExtractInt8(m, {'offset': (9 * 1)}))

                        self._OTPPassBit = np.uint8(ExtractInt8(m, {'offset': (10 * 1)}))
                        self._ModuleID = np.uint8(ExtractInt8(m, {'offset': (11 * 1)}))
                        self._DatabaseID = np.uint8(ExtractInt8(m, {'offset': (12 * 1)}))
                        self._IntensitySync = np.uint8(ExtractInt8(m, {'offset': (13 * 1)}))


                        # Read converted color id
                        _colorIDlsb = np.uint8(ExtractInt8(m, {'offset': (14 * 1)}))
                        _colorIDmsb = np.uint8(ExtractInt8(m, {'offset': (15 * 1)}))
                        self._colorId = (_colorIDlsb & 0xFF)
                        self._colorId += (_colorIDmsb << 8)

                        # Barcode TagNR
                        _barcodeIDlsb = np.uint8(ExtractInt8(m, {'offset': (16 * 1)}))
                        _barcodeIDmsb = np.uint8(ExtractInt8(m, {'offset': (17 * 1)}))
                        self._barcodeId = (_barcodeIDlsb & 0xFF)
                        self._barcodeId += (_barcodeIDmsb << 8)
                        
                    # Old header
                    else:
                        
                        # Read converted color id
                        _colorIDlsb = np.uint8(ExtractInt8(m, {'offset': (12 * 1)}))
                        _colorIDmsb = np.uint8(ExtractInt8(m, {'offset': (13 * 1)}))
                        self._colorId = (_colorIDlsb & 0xFF)
                        self._colorId += (_colorIDmsb << 8)

                        # Barcode TagNR
                        self._barcodeId = np.uint8(ExtractInt8(m, {'offset': (14 * 1)}))
                        

                    # Convert to HSV domain
                    #h, s, v = colorsys.rgb_to_hsv(self._R/255.0, self._G/255.0, self._B/255.0)
                    
                    self._barcode = self._barcodeId
                    self._color = self._colorId

                    # Guess endtype from values received (65535 ?)
                    if (self._barcodeId==0 or (self._barcodeId==255 and self._PixartHeaderLength != 17) or self._barcodeId==65535) and self._colorId != 0:
                        self._decodeType = 'COLOR'
                        self._decodeValue = self._colorId
                    else:
                        self._decodeType = 'BARCODE'
                        self._decodeValue = self._barcodeId


                    self._newTagDataReady = True
                
                    # Color or barcode change
                    if (self._oldcolorId != self._colorId) or (self._oldbarcode != self._barcodeId):
                        # Update gui from variables
                        wx.CallAfter(self.GUIupdate)
                  
                                
    def OnClickClear(self,event):
        self.m_richText_dataLog.Clear()
        self.m_listCtrlIDRead.DeleteAllItems()
        self.BarcodeChangeCounter = 0
        self.m_staticTextLogCounter.SetLabel(str(self.BarcodeChangeCounter))
        
        self.m_richText_dataLogFiltered.Clear()
        self.m_listCtrlIDReadFiltered.DeleteAllItems()
        self.FilteredBarcodeChangeCounter = 0
        self.m_staticTextFilteredLogCounter.SetLabel(str(self.FilteredBarcodeChangeCounter))

    def OnClickRefreshComMac(self,event):
        # List available figures MAC
        self.RefreshComports()
            
    def OnClickRefreshBLE(self,event):
        self.FindClosestDevice('', '')
    
    def UpdateFigureConnectionselection(self, arg=None):

        # BLE Checked
        if self.m_radioBtn_ble.GetValue():
                
            self.m_button_RefreshBLE.Enable()
            self.m_choice_figure_mac.Enable()
            
            self.m_checkBoxFilter.Enable()
            self.m_checkBoxRandomMac.Enable()
                
            self.m_button_RefreshComMac.Disable()
            self.m_choice_comport_utm.Disable()

            if self._bleReady:
                self.m_button_FigureDisconnect.Enable()
                
                self.m_button_RefreshBLE.Disable()
                self.m_choice_figure_mac.Disable()
                self.m_checkBoxFilter.Disable()
                self.m_checkBoxRandomMac.Disable()
            else:
                if self.m_choice_figure_mac.GetSelection() == -1:
                    self.m_button_FigureConnect.Disable()
                else:
                    self.m_button_FigureConnect.Enable()
                
                self.m_button_FigureDisconnect.Disable()


        # UTM Checked
        if self.m_radioBtn_utm.GetValue():

            self.m_button_RefreshBLE.Disable()
            self.m_choice_figure_mac.Disable()
            
            self.m_button_RefreshComMac.Enable()
            self.m_choice_comport_utm.Enable()

            self.m_checkBoxFilter.Disable()
            self.m_checkBoxRandomMac.Disable()
            
            if self._utmReady:
                self.m_button_FigureDisconnect.Enable()
                self.m_button_RefreshComMac.Disable()
                self.m_choice_comport_utm.Disable()
            else:
                if self.m_choice_comport_utm.GetSelection() == -1:
                    self.m_button_FigureConnect.Disable()
                else:
                    self.m_button_FigureConnect.Enable()
                    
                self.m_button_FigureDisconnect.Disable()

        if not self._utmReady and not self._bleReady:
            self.m_radioBtn_ble.Enable()
            self.m_radioBtn_utm.Enable()

        self.m_button_FigureConnect.Refresh()
        self.m_button_FigureDisconnect.Refresh()

        if self._fw == None or self._hw == None:
            self._fw = 'n/a'
            self._hw = 'n/a'
        
        self.m_staticTextFigureFW.SetLabel(self._fw)
        self.m_staticTextFigureHW.SetLabel(self._hw)

    def OnClickConnectionRadioButton(self,event):
        
        self.UpdateFigureConnectionselection()
    
    def OnClickFigureDisconnect(self,event):
        
        self.disconnectBLE()
        self.disconnectUTM()

        # Reset variables
        self._colorId = 65535
        self._barcodeId = 65535
        self._color = 65535

        self._fw = 'n/a'
        self._hw = 'n/a'

        self.UpdateFigureConnectionselection()

        # Update GUI
        wx.CallAfter(self.GUIupdate)
        

    def OnClickFigureConnect(self,event):
        
        if self.m_radioBtn_ble.GetValue():
            self.m_button_FigureConnect.Disable()
            self.m_button_FigureConnect.Refresh()
                
            self.mac = self.m_choice_figure_mac.GetString( self.m_choice_figure_mac.GetSelection())
            self.mac = self.mac[self.mac.find('- ')+2:len(self.mac)]
            
            if not self.connectBLE(self.mac, handledCallback=self.bleReceiveDataHandler):
                self._bleReady = False
                wx.MessageBox('Check dongle installation and driver and that figure is powered On and in BLE pairing mode!', 'Connection Failed', wx.OK | wx.ICON_ERROR)
            else:
                self._bleReady = True

                # Activate notifications
                self.bleActivateTAGnotification(True)

                self.bleActivatePANTSnotification(True)


        if self.m_radioBtn_utm.GetValue():

            self.m_button_FigureConnect.Disable()
            self.m_button_FigureConnect.Refresh()
            
            if not self.connectWTM(port=self.m_choice_comport_utm.GetString( self.m_choice_comport_utm.GetSelection())):
                self._utmReady = False
                wx.MessageBox('Check that figure is powered and in UTM mode. Verify correct serial port is selected.', 'Connection Failed', wx.OK | wx.ICON_ERROR)
            else:
                self._utmReady = True

        if self._bleReady:
            self.m_radioBtn_ble.SetValue(True)
            self.m_radioBtn_utm.SetValue(False)
            self.m_radioBtn_utm.Disable()
            
        if self._utmReady:
            self.m_radioBtn_ble.SetValue(False)
            self.m_radioBtn_utm.SetValue(True)
            self.m_radioBtn_ble.Disable()
            
        self.UpdateFigureConnectionselection()

                
    def connectBLE(self, mac, handledCallback):
        try:
            # Initialize BLE
            self.adapter = pygatt.BGAPIBackend()

            self._mac = mac
            
            # Try to connect to BLE - using static MAC
            self.adapter.start()

            if self.m_checkBoxRandomMac.GetValue():
                self.device = self.adapter.connect(mac, address_type=pygatt.BLEAddressType.random)
            else:
                self.device = self.adapter.connect(mac, address_type=pygatt.BLEAddressType.public)
                
            self._handle = self.device.get_handle('00001624-1212-EFDE-1623-785FEABCD123')

            self.device.subscribe("00001624-1212-EFDE-1623-785FEABCD123",
                         callback=handledCallback)

            self.device.discover_characteristics()

            # Need for new FW to start (05.01.04.0300), we just send a single random byte
            b = [1]
            inserter['uint32'](b, 1, 1)
            b.append(True)
            self.device.char_write_handle(self._handle, bytearray(b), True)
            
            # Wait for BLE to initialize correctly
            timeout = 5
            while not self._bleReady and timeout > 0:
                print("Waiting for connection...")
                timeout = timeout - 1
                time.sleep(1)

            if timeout == 0:
                print('Timeout while trying to connect to ' + mac)
                return False
            else:
                print('BLE connected to ' + mac)

                # Read FW and HW version
                self.bleRequestFWVersion()
                self.bleRequestHWVersion()
        
                return True
        except Exception:
            self._bleReady = False
            self.disconnectBLE()
            print('BLE connection failed to ' + mac + ' (check dongle installation and driver and that figure is powered On and in BLE pairing mode)')
            return False


    def disconnectUTM(self):

        # Signal thread to stop
        self._utmReady = False

        if self.ser is not None:
            if self.ser.isOpen():
                
                # Wait for actual termination (if needed)  
                self.thread.join()  

                # Exit pixart logmode
                b = [0x05, 0x00, 0x15, 0x0D, 0x00]
                self.ser.write(str(bytearray(b)))

                time.sleep(0.1)
                
                # Exit WTM mode  
                b = [0x0A, 0x00, 0x14, 0x4C, 0x45, 0x47, 0x4F, 0x2D, 0x50, 0x54]
                self.ser.write(str(bytearray(b)))

                time.sleep(0.1)
                
                self.ser.close()

            while self.ser.isOpen():
                pass
        
    def Callback(self):
        pass


    def legoColorToRGB(self, color):

        R = 0
        G = 0
        B = 0
        
        if color == 21:
            R = 255
        if color == 23: # Bright blue
            R = 0
            G = 112
            B = 192
        if color == 37:
            G = 255
        if color == 24:
            R = 255
            G = 255
        if color == 28: # Dark green
            R = 64
            G = 119
            B = 50
        if color == 106:
            R = 255
            G = 102
        if color == 107: # Dark Turquois
            R = 0
            G = 176
            B = 240
        if color == 119: # Bright yellow green
            R = 146
            G = 208
            B = 80
        if color == 221: # Bright purple
            R = 255
            G = 0
            B = 255
        if color == 268: # Medium Lilac
            R = 167
            G = 108
            B = 205
        if color == 312:
            R = 170
            G = 125
            B = 85
        if color == 322:
            R = 104
            G = 195
            B = 226
        if color == 324: # medium lavender
            R = 200
            G = 0
            B = 100
        if color == 19:
            R = 255
            G = 255
            B = 255

        return R,G,B
        
    def GUIupdate(self):
        # TAG

        materialIdList = ""

        colorBar1 = None
        colorBar2 = None
        colorBar3 = None
        colorBar4 = None
        colorBar5 = None


        self.m_listBox_DecoID.Clear()

        
        # Find Deco ids from barcode id
        for dict in self.jsonMaterialData['Material array']:
            if dict['Barcode ID'] == self._barcodeId:

                self.m_listBox_DecoID.InsertItems([str(dict['Material ID'])], 0) #add at position zero
                
                if materialIdList == '':
                    materialIdList = str(dict['Material ID'])

                    colorBar1 = dict['Color1']
                    colorBar2 = dict['Color2']
                    colorBar3 = dict['Color3']
                    colorBar4 = dict['Color4']
                    colorBar5 = dict['Color5']
                    
                else:
                    materialIdList = materialIdList + '\n' + str(dict['Material ID'])

        if materialIdList == '':
            materialIdList = "Not found"
            self.m_listBox_DecoID.InsertItems([materialIdList], 0)

        if self._barcode == 65535 or self._barcode == -1:
            self.m_staticText_BarcodeID.SetLabel('NONE')
            self.m_staticText_SystemID.SetLabel('NONE')
        else:
            self.m_staticText_BarcodeID.SetLabel(str(self._barcode))
            self.m_staticText_SystemID.SetLabel(str(self._DatabaseID))

        # Do not support system information over BLE
        if self._bleReady:
            self.m_staticText_SystemID.SetLabel('n/a')

        if self._color == 65535 or self._color == -1:
            self.m_staticText_ColorID.SetLabel('NONE')
            self.m_panelColor.SetBackgroundColour(wx.SystemSettings.GetColour( wx.SYS_COLOUR_APPWORKSPACE ))
        else: 
            self.m_staticText_ColorID.SetLabel(str(self._color))
            
            # Convert standard color reading to RGB
            colorRGB = self.legoColorToRGB(self._color)
            self.m_panelColor.SetBackgroundColour((colorRGB[0], colorRGB[1], colorRGB[2]))
            
        self.m_panelColor.Refresh()
        

        # Lookup colors
        if colorBar1 is not None:
            colorRGB = self.legoColorToRGB(colorBar1)
            self.m_staticTextColorBar1.SetBackgroundColour((colorRGB[0], colorRGB[1], colorRGB[2]))
            self.m_staticTextColorBar1.SetLabel('Color #1 \t ' + str(colorBar1))
        else:
            self.m_staticTextColorBar1.SetBackgroundColour(wx.SystemSettings.GetColour( wx.SYS_COLOUR_APPWORKSPACE ))
            self.m_staticTextColorBar1.SetLabel('')
            
        if colorBar2 is not None:
            colorRGB = self.legoColorToRGB(colorBar2)
            self.m_staticTextColorBar2.SetBackgroundColour((colorRGB[0], colorRGB[1], colorRGB[2]))
            self.m_staticTextColorBar2.SetLabel('Color #2 \t ' + str(colorBar2))
        else:
            self.m_staticTextColorBar2.SetBackgroundColour(wx.SystemSettings.GetColour( wx.SYS_COLOUR_APPWORKSPACE ))
            self.m_staticTextColorBar2.SetLabel('')
            
        if colorBar3 is not None:
            colorRGB = self.legoColorToRGB(colorBar3)
            self.m_staticTextColorBar3.SetBackgroundColour((colorRGB[0], colorRGB[1], colorRGB[2]))
            self.m_staticTextColorBar3.SetLabel('Color #3 \t ' + str(colorBar3))
        else:
            self.m_staticTextColorBar3.SetBackgroundColour(wx.SystemSettings.GetColour( wx.SYS_COLOUR_APPWORKSPACE ))
            self.m_staticTextColorBar3.SetLabel('')
            
        if colorBar4 is not None:
            colorRGB = self.legoColorToRGB(colorBar4)
            self.m_staticTextColorBar4.SetBackgroundColour((colorRGB[0], colorRGB[1], colorRGB[2]))
            self.m_staticTextColorBar4.SetLabel('Color #4 \t ' + str(colorBar4))
        else:
            self.m_staticTextColorBar4.SetBackgroundColour(wx.SystemSettings.GetColour( wx.SYS_COLOUR_APPWORKSPACE ))
            self.m_staticTextColorBar4.SetLabel('')
            
        if colorBar5 is not None:
            colorRGB = self.legoColorToRGB(colorBar5)
            self.m_staticTextColorBar5.SetBackgroundColour((colorRGB[0], colorRGB[1], colorRGB[2]))
            self.m_staticTextColorBar5.SetLabel('Color #5 \t ' + str(colorBar5))
        else:
            self.m_staticTextColorBar5.SetBackgroundColour(wx.SystemSettings.GetColour( wx.SYS_COLOUR_APPWORKSPACE ))
            self.m_staticTextColorBar5.SetLabel('')
            
        self.m_staticTextColorBar1.Refresh()
        self.m_staticTextColorBar2.Refresh()
        self.m_staticTextColorBar3.Refresh()
        self.m_staticTextColorBar4.Refresh()
        self.m_staticTextColorBar5.Refresh()


        
        if bool(self._pants & (0x01 << 0x00)):
            colorRGB = self.legoColorToRGB(28)
            self.m_staticTextPants1.SetBackgroundColour((colorRGB[0], colorRGB[1], colorRGB[2]))
        else:
            self.m_staticTextPants1.SetBackgroundColour(wx.SystemSettings.GetColour( wx.SYS_COLOUR_APPWORKSPACE ))
            
        if bool(self._pants & (0x01 << 0x01)):
            colorRGB = self.legoColorToRGB(28)
            self.m_staticTextPants2.SetBackgroundColour((colorRGB[0], colorRGB[1], colorRGB[2]))
        else:
            self.m_staticTextPants2.SetBackgroundColour(wx.SystemSettings.GetColour( wx.SYS_COLOUR_APPWORKSPACE ))

        if bool(self._pants & (0x01 << 0x02)):
            colorRGB = self.legoColorToRGB(28)
            self.m_staticTextPants3.SetBackgroundColour((colorRGB[0], colorRGB[1], colorRGB[2]))
        else:
            self.m_staticTextPants3.SetBackgroundColour(wx.SystemSettings.GetColour( wx.SYS_COLOUR_APPWORKSPACE ))

        if bool(self._pants & (0x01 << 0x03)):
            colorRGB = self.legoColorToRGB(28)
            self.m_staticTextPants4.SetBackgroundColour((colorRGB[0], colorRGB[1], colorRGB[2]))
        else:
            self.m_staticTextPants4.SetBackgroundColour(wx.SystemSettings.GetColour( wx.SYS_COLOUR_APPWORKSPACE ))

        if bool(self._pants & (0x01 << 0x04)):
            colorRGB = self.legoColorToRGB(28)
            self.m_staticTextPants5.SetBackgroundColour((colorRGB[0], colorRGB[1], colorRGB[2]))
        else:
            self.m_staticTextPants5.SetBackgroundColour(wx.SystemSettings.GetColour( wx.SYS_COLOUR_APPWORKSPACE ))

        if bool(self._pants & (0x01 << 0x05)):
            colorRGB = self.legoColorToRGB(28)
            self.m_staticTextPants6.SetBackgroundColour((colorRGB[0], colorRGB[1], colorRGB[2]))
        else:
            self.m_staticTextPants6.SetBackgroundColour(wx.SystemSettings.GetColour( wx.SYS_COLOUR_APPWORKSPACE ))
            
        self.m_staticTextPants1.Refresh()
        self.m_staticTextPants2.Refresh()
        self.m_staticTextPants3.Refresh()
        self.m_staticTextPants4.Refresh()
        self.m_staticTextPants5.Refresh()
        self.m_staticTextPants6.Refresh()
        
    def disconnectBLE(self):

        self._bleReady = False
        
        # Terminate BLE
        if self.adapter is not None:
            self.adapter.stop()

        
    # Update BLE List
    def FindClosestDevice(self, devices, msd):

        self.m_choice_figure_mac.Clear()
        
        self.m_button_RefreshBLE.Disable()
        self.m_choice_figure_mac.Disable()

        
        print("Start searching for BLE advertising devices, please wait...")
            
        # Initialize BLE
        self.disconnectBLE()
        try:
            self.adapter = pygatt.BGAPIBackend()
            self.adapter.start()
        except:
            #No BGAPI compatible device detected
            wx.MessageBox('Could not find BLE dongle! Recheck that dongle is inserted in the USB port and try again.', 'BLE dongle missing', wx.OK | wx.ICON_ERROR)
            print("Could not find BLE dongle! Recheck that dongle is inserted and try again.")
            self.m_button_RefreshBLE.Enable()
            return
            
        devices = self.adapter.scan(timeout=3, active=True)
        
        print("_________________________________________________________________________________")
        print("ID\tNAME\t\tMAC\t\t\tRSSI\tLEGO ID")
        
        devmac = []
        viewlist = []

        for d in devices:
            # Filter on LEGO manufactorer id

            connectable_advertisement_packet = ''
            try:
                connectable_advertisement_packet = d['packet_data']['connectable_advertisement_packet']['manufacturer_specific_data']
            except:
                pass
                
            if self.m_checkBoxFilter.GetValue():
                if connectable_advertisement_packet == b'\x97\x03\x00\x43\x03\xff\xff\x00' or connectable_advertisement_packet == b'\x97\x03\x00\x43\x0a\x00\x41\x00' or connectable_advertisement_packet == b'\x97\x03\x00\x45\x03\xff\xff\x00' or connectable_advertisement_packet == b'\x97\x03\x00\x44\x01\x00\x41\x00':
                    print(str(len(devmac))+ ')\t' + d['name'] + '\t' + str(d['address']) + '\t' + str(d['rssi']) + '\t' + str(binascii.hexlify(d['packet_data']['connectable_advertisement_packet']['manufacturer_specific_data'])))
                    devmac.append(d['address'])
                    viewlist.append(d['name'] + ' - ' + d['address'])
            else:
                print(str(len(devmac)) + ')\t' + d['name'] + '\t' + str(d['address']) + '\t' + str(d['rssi']) + '\t' + str(binascii.hexlify(connectable_advertisement_packet)))
                devmac.append(d['address'])
                viewlist.append(d['name'] + ' - ' + d['address'])
            
        self.disconnectBLE()
        
        print("_________________________________________________________________________________")
        print("Found " + str(len(devmac)) + " devices")

        self.m_choice_figure_mac.SetItems(viewlist)

        if(len(viewlist) > 0):
            self.m_choice_figure_mac.SetSelection(0)
            self.m_choice_figure_mac.Enable()
            self.m_button_FigureConnect.Enable()
        else:
            self.m_choice_figure_mac.Disable()
            self.m_button_FigureConnect.Disable()
            wx.MessageBox('Check that figure is powered ON and in BLE pairing mode!', 'No devices found', wx.OK | wx.ICON_ERROR)

        self.m_button_RefreshBLE.Enable()

        self.UpdateFigureConnectionselection()

             
    # Activate notifications for PortId=3 - TAG Sensor
    def bleActivateTAGnotification(self, enable=True):
        
        _msg_len = 0x0A
        _nwk_id  = 0x00
        _cmd_id  = 0x41
        
        p = 1       # PortID
        m = 0x00    # Mode
        di = 0x01   # DeltaInterval
        if enable:
            ne = 0x01   # Notification Enabled
        else:
            ne = 0x00   # Notification Disabled
        wait_for_reply = True

        b = [_msg_len, _nwk_id, _cmd_id, p, m, di]
        inserter['uint32'](b, 5, 1)
        b.append(True)
        if self._bleReady:
            self.device.char_write_handle(self._handle, bytearray(b), wait_for_reply)
            
    def bleActivatePANTSnotification(self, enable=True):
        
        _msg_len = 0x0A
        _nwk_id  = 0x00
        _cmd_id  = 0x41
        
        p = 2       # PortID
        m = 0x00    # Mode
        di = 0x01   # DeltaInterval
        if enable:
            ne = 0x01   # Notification Enabled
        else:
            ne = 0x00   # Notification Disabled
        wait_for_reply = True

        b = [_msg_len, _nwk_id, _cmd_id, p, m, di]
        inserter['uint32'](b, 5, 1)
        b.append(True)
        self.device.char_write_handle(self._handle, bytearray(b), wait_for_reply)
   
    def bleRequestFWVersion(self):
        _msg_len = 0x05
        _nwk_id  = 0x00
        _cmd_id  = 0x01 # HUB Properties
        #                               0x03=FW Version  0x05=RequestUpdate
        b = [_msg_len, _nwk_id, _cmd_id, 0x03, 0x05]
        self.device.char_write_handle(self._handle, bytearray(b), True)
        
    def bleRequestHWVersion(self):
        _msg_len = 0x05
        _nwk_id  = 0x00
        _cmd_id  = 0x01 # HUB Properties
        #                               0x04=HW Version  0x05=RequestUpdate
        b = [_msg_len, _nwk_id, _cmd_id, 0x04, 0x05]
        self.device.char_write_handle(self._handle, bytearray(b), True)
        
    # Handler called whenever BLE data is received (runs in own thread)
    def bleReceiveDataHandler(self, e, m):

        #print("Received data: %s" % hexlify(m))
        msgType = m[2]
        p = m[3]
        #print("Message type: %s" % (msgType))
        
        if _messages['HubAttachedIO'] == msgType and p==3: # TODO: Better way to identify init complete?
            #print("Handle io attach event")
            # Signal main thread we are ready
            self._bleReady = True
        
        ret = 0
        for b in reversed(m[4:]):
           ret = (ret<<8) + b
           
        #print("Port id: %s" % (p))
           
        if _messages['HubProperties'] == msgType:

            #print('Received HubProperties\r\n')
            if p == 3: # FW
                self._fw = ExtractLEGOVersion(m, {'offset': 5})           
            if p == 4: # HW
                self._hw = ExtractLEGOVersion(m, {'offset': 5})

        # Pants
        if _messages['PortValueSingle'] == msgType and p==2: #change to P==4 if FW prior to 0.9
            self._pants = np.uint8(ExtractInt8(m, {'offset': 4}))
            self._newPantsDataReady = True
            #print('Received Pants data: ' + str(self._pants) + '\r\n')
            raw = self._pants

            self._newPantsDataReady = True

            wx.CallAfter(self.GUIupdate)
            
            print('{:%d.%m.%Y %H:%M:%S}'.format(datetime.now()) + '\t[PANTS]\t1:' + str(bool(raw & (0x01 << 0x00)))+ '\t2:' + str(bool(raw & (0x01 << 0x01)))+ '\t3:' + str(bool(raw & (0x01 << 0x02)))+ '\t4:' + str(bool(raw & (0x01 << 0x03)))+ '\t5:' + str(bool(raw & (0x01 << 0x04))) + '\t6:' + str(bool(raw & (0x01 << 0x05))) + '\t(raw=' + str(raw) + ')\n')

            
        # Hardcoded support for TAG sensor.
        if _messages['PortValueSingle'] == msgType and p==1:
 
            # Save timestamp
            self._newTagDataReadyTS = time.time()
            
            self._oldcolorId = self._colorId
            self._oldbarcode = self._barcodeId
            
            length = 2
            # Read Color Code
            ret = ExtractInt16(m, {'offset': 4 + (1 * length)})
            self._colorId = ret
            # Read Barcode
            ret = ExtractInt16(m, {'offset': 4 + (0 * length)})
            self._barcodeId = ret


            self._barcode = self._barcodeId
            self._color = self._colorId
                
            # Guess endtype from values received
            if (self._barcodeId==-1 or self._barcodeId==65535) and self._colorId != 0:
                self._decodeType = 'COLOR'
                self._decodeValue = self._colorId
            else:
                self._decodeType = 'BARCODE'
                self._decodeValue = self._barcodeId

            # Color change
            if (self._oldcolorId != self._colorId) or (self._oldbarcode != self._barcodeId):
                # Update gui from variables
                wx.CallAfter(self.GUIupdate)

            self._newTagDataReady = True
            
# Run the program
if __name__ == "__main__":
    app = wx.App(False)
    frame = MainFrame(None)
    frame.Show()
    app.MainLoop()
