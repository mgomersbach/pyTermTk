#!/usr/bin/env python3

# MIT License
#
# Copyright (c) 2021 Eugenio Parodi <ceccopierangiolieugenio AT googlemail DOT com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from TermTk.TTkCore.cfg import TTkCfg
from TermTk.TTkCore.constant import TTkK
from TermTk.TTkCore.log import TTkLog
from TermTk.TTkCore.signal import pyTTkSlot, pyTTkSignal
from TermTk.TTkCore.helper import TTkHelper
from TermTk.TTkCore.string import TTkString
from TermTk.TTkLayouts.gridlayout import TTkGridLayout
from TermTk.TTkWidgets.widget import TTkWidget
from TermTk.TTkWidgets.list_ import TTkList
from TermTk.TTkWidgets.lineedit import TTkLineEdit
from TermTk.TTkWidgets.resizableframe import TTkResizableFrame

class TTkComboBox(TTkWidget):
    ''' TTkComboBox:

    Editable = False
    ::

         [ - select -  ^]

    Editable = True
    ::

         [ Text       [^]

    :param list: the list of the items selectable by this combobox, defaults to "[]"
    :type list: list(str), optional

    :param insertPolicy: the policy used to determine where user-inserted items should appear in the combobox, defaults to :class:`~TermTk.TTkCore.constant.TTkConstant.InsertPolicy.InsertAtBottom`
    :type insertPolicy: :class:`~TermTk.TTkCore.constant.TTkConstant.InsertPolicy`, optional

    :param textAlign: This enum type is used to define the text alignment, defaults to :class:`~TermTk.TTkCore.constant.TTkConstant.Alignment.CENTER_ALIGN`
    :tye textAlign: :class:`~TermTk.TTkCore.constant.TTkConstant.Alignment`, optional

    :param editable: This property holds whether the combo box can be edited by the user, defaults to False
    :type editable: bool, optional
    '''
    __slots__ = ('_list', '_id', '_lineEdit', '_listw', '_editable', '_insertPolicy', '_textAlign', '_popupFrame',
        #signals
        'currentIndexChanged', 'currentTextChanged', 'editTextChanged')
    def __init__(self, *args, **kwargs):
        # Define Signals
        self.currentIndexChanged = pyTTkSignal(int)
        self.currentTextChanged  = pyTTkSignal(str)
        self.editTextChanged     = pyTTkSignal(str)
        TTkWidget.__init__(self, *args, **kwargs)
        # self.checked = pyTTkSignal()
        self._lineEdit = TTkLineEdit(parent=self)
        self._list = kwargs.get('list', [] )
        self._insertPolicy = kwargs.get('insertPolicy', TTkK.InsertAtBottom )
        self._lineEdit.returnPressed.connect(self._lineEditChanged)
        self._textAlign = kwargs.get('textAlign', TTkK.CENTER_ALIGN)
        self._id = -1
        self._popupFrame = None
        self.setEditable(kwargs.get('editable', False ))
        self.setMinimumSize(5, 1)
        self.setMaximumHeight(1)

    def _lineEditChanged(self):
        text = self._lineEdit.text()
        self._id=-1
        if text in self._list:
            self._id = self._list.index(text)
        elif self._insertPolicy ==  TTkK.NoInsert:
            pass
        elif self._insertPolicy ==  TTkK.InsertAtTop:
            self._id=0
            self._list.insert(0,text)
        # elif self._insertPolicy ==  TTkK.InsertAtCurrent:
        #     pass
        elif self._insertPolicy ==  TTkK.InsertAtBottom:
            self._id=len(self._list)
            self._list.append(text)
        # elif self._insertPolicy ==  TTkK.InsertAfterCurrent:
        #     pass
        # elif self._insertPolicy ==  TTkK.InsertBeforeCurrent:
        #     pass
        # elif self._insertPolicy ==  TTkK.InsertAlphabetically:
        #     pass
        else:
            pass
        self.currentIndexChanged.emit(self._id)
        self.currentTextChanged.emit(text)
        self.editTextChanged.emit(text)

    def textAlign(self):
        '''his property holds the displayed text alignment

        :return: :class:`~TermTk.TTkCore.constant.TTkConstant.Alignment`
        '''
        return self._textAlign

    def setTextAlign(self, align):
        '''This property holds the displayed text alignment

        :param align:
        :type align: :class:`~TermTk.TTkCore.constant.TTkConstant.Alignment`
        '''
        if self._textAlign != align:
            self._textAlign = align
            self.update()

    def addItem(self, text, userData=None):
        '''addItem

        Adds an item to the combobox with the given text, and containing the specified userData (stored in the Qt::UserRole). The item is appended to the list of existing items.
        '''
        self._list.append(text)
        self.update()

    def addItems(self,items):
        '''addItems'''
        for item in items:
            self.addItem(item)

    def clear(self):
        '''clear'''
        self._lineEdit.setText("")
        self._list = []
        self._id = -1
        self.update()

    def lineEdit(self):
        return self._lineEdit if self._editable else None

    def resizeEvent(self, w: int, h: int):
        w,h = self.size()
        self._lineEdit.setGeometry(1,0,w-4,h)

    def paintEvent(self):
        if not self.isEnabled():
            borderColor = TTkCfg.theme.comboboxBorderColorDisabled
            color       = TTkCfg.theme.comboboxContentColorDisabled
        elif self.hasFocus():
            borderColor = TTkCfg.theme.comboboxBorderColorFocus
            color       = TTkCfg.theme.comboboxContentColorFocus
        else:
            borderColor = TTkCfg.theme.comboboxBorderColor
            color       = TTkCfg.theme.comboboxContentColor
        if self._id == -1:
            text = "- select -"
        else:
            text = self._list[self._id]
        w = self.width()

        self._canvas.drawTTkString(pos=(1,0), text=TTkString(text), width=w-3, alignment=self._textAlign, color=color)
        self._canvas.drawText(pos=(0,0), text="[",    color=borderColor)
        if self._editable:
            self._canvas.drawText(pos=(w-3,0), text="[^]", color=borderColor)
        else:
            self._canvas.drawText(pos=(w-2,0), text="^]", color=borderColor)

    def currentText(self):
        '''currentText'''
        if self._editable:
            return self._lineEdit.text()
        elif self._id >= 0:
            return self._list[self._id]
        return ""

    def currentIndex(self):
        '''currentIndex'''
        return self._id

    @pyTTkSlot(int)
    def setCurrentIndex(self, index):
        '''setCurrentIndex'''
        if index > len(self._list)-1: return
        self._id = index
        if self._editable:
            self._lineEdit.setText(self._list[self._id])
        else:
            self.currentTextChanged.emit(self._list[self._id])
        self.currentIndexChanged.emit(self._id)
        self.update()

    @pyTTkSlot(str)
    def setCurrentText(self, text):
        '''setCurrentText'''
        if self._editable:
            self.setEditText(text)
        else:
            if id := self._list.index(text):
                self.setCurrentIndex(id)

    @pyTTkSlot(str)
    def setEditText(self, text):
        '''setEditText'''
        if self._editable:
            self._lineEdit.setText(text)

    def insertPolicy(self):
        '''insertPolicy'''
        return self._insertPolicy

    def setInsertPolicy(self, ip):
        '''setInsertPolicy'''
        self._insertPolicy = ip

    def isEditable(self):
        '''isEditable'''
        return self._editable

    def setEditable(self, editable):
        '''setEditable'''
        self._editable = editable
        if editable:
            self._lineEdit.show()
            self.setFocusPolicy(TTkK.ClickFocus)
        else:
            self._lineEdit.hide()
            self.setFocusPolicy(TTkK.ClickFocus + TTkK.TabFocus)

    @pyTTkSlot(str)
    def _callback(self, label):
        if self._editable:
            self._lineEdit.setText(label)
        self.setCurrentIndex(self._list.index(label))
        TTkHelper.removeOverlayAndChild(self._popupFrame)
        self._popupFrame = None
        self.setFocus()
        self.update()

    def _pressEvent(self):
        frameHeight = len(self._list) + 2
        frameWidth = self.width()
        if frameHeight > 20: frameHeight = 20
        if frameWidth  < 20: frameWidth = 20

        self._popupFrame = TTkResizableFrame(layout=TTkGridLayout(), size=(frameWidth,frameHeight))
        TTkHelper.overlay(self, self._popupFrame, 0, 0)
        listw = TTkList(parent=self._popupFrame)
        TTkLog.debug(f"{self._list}")
        for item in self._list:
            listw.addItem(item)
        if self._id != -1:
            listw.setCurrentRow(self._id)
        listw.textClicked.connect(self._callback)
        listw.viewport().setFocus()
        self.update()
        return True

    def mousePressEvent(self, evt):
        self._pressEvent()
        return True

    def keyEvent(self, evt):
        if ( evt.type == TTkK.Character and evt.key==" " ) or \
           ( evt.type == TTkK.SpecialKey and evt.key in [TTkK.Key_Enter,TTkK.Key_Down] ):
            self._pressEvent()
            return True
        return False

    def focusInEvent(self):
        if self._editable:
            self._lineEdit.setFocus()

    _ttkProperties = {
        'Editable' : {
                'init': {'name':'editable', 'type':bool } ,
                'get':  {'cb':isEditable,   'type':bool } ,
                'set':  {'cb':setEditable,  'type':bool } },
        'Text Align.' : {
                'init': {'name':'textAlign', 'type':'singleflag',
                    'flags': {
                        'None'   : TTkK.Alignment.NONE,
                        'Left'   : TTkK.Alignment.LEFT_ALIGN,
                        'Right'  : TTkK.Alignment.RIGHT_ALIGN,
                        'Center' : TTkK.Alignment.CENTER_ALIGN,
                        'Justify': TTkK.Alignment.JUSTIFY } },
                'get':  {'cb':textAlign,    'type':'singleflag',
                    'flags': {
                        'None'   : TTkK.Alignment.NONE,
                        'Left'   : TTkK.Alignment.LEFT_ALIGN,
                        'Right'  : TTkK.Alignment.RIGHT_ALIGN,
                        'Center' : TTkK.Alignment.CENTER_ALIGN,
                        'Justify': TTkK.Alignment.JUSTIFY } } ,
                'set':  {'cb':setTextAlign, 'type':'singleflag',
                    'flags': {
                        'None'   : TTkK.Alignment.NONE,
                        'Left'   : TTkK.Alignment.LEFT_ALIGN,
                        'Right'  : TTkK.Alignment.RIGHT_ALIGN,
                        'Center' : TTkK.Alignment.CENTER_ALIGN,
                        'Justify': TTkK.Alignment.JUSTIFY } } },
        'Insert Policy' : {
                'init': {'name':'insertPolicy', 'type':'singleflag',
                    'flags': {
                        'No Insert'   : TTkK.InsertPolicy.NoInsert,
                        'At Top'      : TTkK.InsertPolicy.InsertAtTop,
                        'At Bottom'   : TTkK.InsertPolicy.InsertAtBottom } },
                'get':  {'cb':insertPolicy,    'type':'singleflag',
                    'flags': {
                        'No Insert'   : TTkK.InsertPolicy.NoInsert,
                        'At Top'      : TTkK.InsertPolicy.InsertAtTop,
                        'At Bottom'   : TTkK.InsertPolicy.InsertAtBottom } },
                'set':  {'cb':setInsertPolicy, 'type':'singleflag',
                    'flags': {
                        'No Insert'   : TTkK.InsertPolicy.NoInsert,
                        'At Top'      : TTkK.InsertPolicy.InsertAtTop,
                        'At Bottom'   : TTkK.InsertPolicy.InsertAtBottom } } },
    }