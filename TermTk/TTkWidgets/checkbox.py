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
from TermTk.TTkCore.string import TTkString
from TermTk.TTkCore.signal import pyTTkSignal
from TermTk.TTkWidgets.widget import *

class TTkCheckbox(TTkWidget):
    '''
    **Checked**
    ::

        [X]CheckBox

    **Unchecked**
    ::

        [ ]CheckBox

    **Partially Checked**
    ::

        [/]CheckBox

    :Demo: `formwidgets.py <https://github.com/ceccopierangiolieugenio/pyTermTk/blob/main/demo/showcase/formwidgets.py>`_

    :param str text: the text shown on the checkbox, defaults to ""
    :type text: str, optional
    :param bool checked: Checked status, defaults to "False"
    :type checked: bool, optional

    +-----------------------------------------------------------------------------------------------+
    | `Signals <https://ceccopierangiolieugenio.github.io/pyTermTk/tutorial/003-signalslots.html>`_ |
    +-----------------------------------------------------------------------------------------------+

        .. py:method:: clicked(checked)
            :signal:

            This signal is emitted when the button is activated

            :param checked: True if checked otherwise False
            :type checked: bool
            :param checkStatus: The state of the checkbox
            :type checkStatus: :class:`~TermTk.TTkCore.constant.TTkConstant.CheckState`
            :param tristate: | This property holds whether the checkbox is a tri-state checkbox
                             | The default is false, i.e., the checkbox has only two states.
            :type tristate: bool

        .. py:method:: stateChanged(state)
            :signal:

            This signal is emitted whenever the checkbox's state changes, i.e., whenever the user checks or unchecks it.

            :param state: state of the checkbox
            :type state: :class:`~TermTk.TTkCore.constant.TTkConstant.CheckState`

     '''
    __slots__ = (
        '_checkStatus', '_text', '_tristate',
        # Signals
        'clicked', 'stateChanged'
        )
    def __init__(self, *args, **kwargs):
        TTkWidget.__init__(self, *args, **kwargs)
        # Define Signals
        self.stateChanged = pyTTkSignal(TTkK.CheckState)
        self.clicked = pyTTkSignal(bool)
        if 'checkStatus' in kwargs:
            self._checkStatus = kwargs.get('checkStatus', TTkK.Unchecked )
        else:
            self._checkStatus = TTkK.Checked if kwargs.get('checked', False ) else TTkK.Unchecked
        self._tristate = kwargs.get('tristate', False)
        self._text = TTkString(kwargs.get('text', '' ))
        self.setMinimumSize(3 + len(self._text), 1)
        self.setMaximumHeight(1)
        self.setFocusPolicy(TTkK.ClickFocus + TTkK.TabFocus)

    def text(self):
        ''' This property holds the text shown on the checkhox

        :return: :class:`~TermTk.TTkCore.string.TTkString`
        '''
        return self._text

    def setText(self, text):
        ''' This property holds the text shown on the checkhox

        :param text:
        :type text: :class:`~TermTk.TTkCore.string.TTkString`
        '''
        if self._text == text: return
        self._text = TTkString(text)
        self.setMinimumSize(3 + len(self._text), 1)
        self.update()

    def isTristate(self):
        ''' This property holds whether the checkbox is a tri-state checkbox

        :return: bool
        '''
        return self._tristate

    def setTristate(self, tristate):
        ''' Enable/Disable the tristate property

        :param tristate:
        :type tristate: bool
        '''
        if tristate == self._tristate: return
        self._tristate = tristate
        self.update()

    def isChecked(self):
        ''' This property holds whether the checkbox is checked

        :return: bool - True if :class:`~TermTk.TTkCore.constant.TTkConstant.CheckState.Checked` or :class:`~TermTk.TTkCore.constant.TTkConstant.CheckState.PartiallyChecked`
        '''
        return self._checkStatus != TTkK.Unchecked

    def setChecked(self, state):
        ''' Set the check status

        :param state:
        :type state: bool
        '''
        self.setCheckState(TTkK.Checked if state else TTkK.Unchecked)

    def checkState(self):
        ''' Retrieve the state of the checkbox

        :return: :class:`~TermTk.TTkCore.constant.TTkConstant.CheckState` : the checkbox status
        '''
        return self._checkStatus

    def setCheckState(self, state):
        ''' Sets the checkbox's check state.

        :param state: state of the checkbox
        :type state: :class:`~TermTk.TTkCore.constant.TTkConstant.CheckState`
        '''
        if self._checkStatus == state: return
        if state==TTkK.PartiallyChecked and not self._tristate: return
        self._checkStatus = state
        self.update()

    def paintEvent(self):
        if not self.isEnabled():
            textColor   = TTkCfg.theme.checkboxTextColor
            borderColor = TTkCfg.theme.textColorDisabled
            xColor = TTkCfg.theme.textColorDisabled
        elif self.hasFocus():
            borderColor = TTkCfg.theme.checkboxBorderColorFocus
            textColor   = TTkCfg.theme.checkboxTextColorFocus
            xColor      = TTkCfg.theme.checkboxContentColorFocus
        else:
            borderColor = TTkCfg.theme.checkboxBorderColor
            textColor   = TTkCfg.theme.checkboxTextColor
            xColor      = TTkCfg.theme.checkboxContentColor
        self._canvas.drawText(pos=(0,0), color=borderColor ,text="[ ]")
        self._canvas.drawText(pos=(3,0), color=textColor ,text=self._text)
        text = {
            TTkK.Checked :   "X",
            TTkK.Unchecked : " ",
            TTkK.PartiallyChecked: "/"}.get(self._checkStatus, " ")
        self._canvas.drawText(pos=(1,0), color=xColor ,text=text)

    def _pressEvent(self):
        self._checkStatus = {
            TTkK.Unchecked:        TTkK.PartiallyChecked,
            TTkK.PartiallyChecked: TTkK.Checked,
            TTkK.Checked:          TTkK.Unchecked,
        }.get(self._checkStatus,TTkK.Unchecked)
        if not self._tristate and self._checkStatus == TTkK.PartiallyChecked:
            self._checkStatus = TTkK.Checked
        self.clicked.emit(self._checkStatus!=TTkK.Unchecked)
        self.stateChanged.emit(self._checkStatus)
        self.update()
        return True

    def mousePressEvent(self, evt):
        self._pressEvent()
        return True

    def keyEvent(self, evt):
        if ( evt.type == TTkK.Character and evt.key==" " ) or \
           ( evt.type == TTkK.SpecialKey and evt.key == TTkK.Key_Enter ):
            self._pressEvent()
            return True
        return False

    _ttkProperties = {
        'Text' : {
                'init': {'name':'text', 'type':TTkString } ,
                'get':  {'cb':text,     'type':TTkString } ,
                'set':  {'cb':setText,  'type':TTkString } },
        'Tristate' : {
                'init': {'name':'tristate', 'type':bool } ,
                'get':  {'cb':isTristate,   'type':bool } ,
                'set':  {'cb':setTristate,  'type':bool } },
        'Checked' : {
                'init': {'name':'checked', 'type':bool } ,
                'get':  {'cb':isChecked,   'type':bool } ,
                'set':  {'cb':setChecked,  'type':bool } },
        'Check State' : {
                'init': { 'name':'checked', 'type':'singleflag',
                    'flags': {
                        'Checked'          : TTkK.Checked    ,
                        'Unchecked'        : TTkK.Unchecked  ,
                        'Partially Checked': TTkK.PartiallyChecked } },
                'get' : { 'cb':checkState,      'type':'singleflag',
                    'flags': {
                        'Checked'          : TTkK.Checked    ,
                        'Unchecked'        : TTkK.Unchecked  ,
                        'Partially Checked': TTkK.PartiallyChecked } },
                'set' : { 'cb':setCheckState,   'type':'singleflag',
                    'flags': {
                        'Checked'          : TTkK.Checked    ,
                        'Unchecked'        : TTkK.Unchecked  ,
                        'Partially Checked': TTkK.PartiallyChecked } },
         },
    }
