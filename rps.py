import wx
import random


class BorderPanel(wx.Panel):
    """A panel that draws a rounded rectangle background with a colored border.
    Use it to create a polished, fancy bordered container.
    """
    def __init__(self, parent, background="#FFFFFF", border_color="#FFD166", border_width=4, radius=12, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self._background = background
        self._border_color = border_color
        self._border_width = border_width
        self._radius = radius
        self.Bind(wx.EVT_PAINT, self._on_paint)

    def _on_paint(self, event):
        dc = wx.BufferedPaintDC(self)
        gc = wx.GraphicsContext.Create(dc)
        w, h = self.GetClientSize()
        
        gc.SetBrush(wx.Brush(self._background))
        gc.SetPen(wx.Pen(self._border_color, self._border_width))
        bw = self._border_width
        try:
            gc.DrawRoundedRectangle(bw / 2, bw / 2, w - bw, h - bw, self._radius)
        except Exception:
            
            gc.DrawRectangle(bw / 2, bw / 2, w - bw, h - bw)


FULLSCREEN_ON_START = False

# Colors palette (pale cyan bg, indigo accent, neutral text)
OUTER_BG = "#F0F9FF"        # pale cyan
CONTAINER_BORDER = "#2563EB" # indigo blue (accent)
CONTAINER_BG = "#FFF8E6"    # warm cream (softer and warmer than pure white)
TITLE_COLOR = "#0F172A"     # dark navy for title
RESULT_BG = "#ECFDF5"       # pale green for results
RESULT_FG = "#065F46"       # dark green for result text
INFO_COLOR = "#0F172A"      # neutral dark color for info text


choices = ["✊ Rock", "✋ Paper", "✌️ Scissors"]

class RockPaperScissors(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title="Rock Paper Scissors Simulator", size=(580, 480))
        panel = wx.Panel(self)
        
        self.SetBackgroundColour("#0A3D62")  # deep navy background
        font = wx.Font(16, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        title_font = wx.Font(22, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        result_font = wx.Font(20, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        btn_font = wx.Font(16, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)

        
        container = BorderPanel(panel, background=CONTAINER_BG, border_color=CONTAINER_BORDER, border_width=3, radius=14)
        container.SetMinSize((520, 420))
        
        title = wx.StaticText(container, label="✊ROCK✋PAPER✌️SCISSORS", style=wx.ALIGN_CENTER)
        title.SetForegroundColour(TITLE_COLOR)
        title.SetFont(title_font)

        
        self.result = wx.StaticText(container, label="", style=wx.ALIGN_CENTER)
        self.result.SetForegroundColour(RESULT_FG)
        self.result.SetBackgroundColour(RESULT_BG)
        self.result.SetFont(result_font)
        
       
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        btn_colors = ["#EF4444", CONTAINER_BORDER, "#10B981"]  # rock(red), paper(indigo), scissors(green)
        for index, name in enumerate(choices):
            btn = wx.Button(container, label=name, size=(160, 80))
            btn.SetBackgroundColour(btn_colors[index])
            btn.SetForegroundColour("white")
            btn.SetFont(btn_font)
            btn.SetToolTip(f"Choose {name.split(maxsplit=1)[1]}")
            btn.Bind(wx.EVT_BUTTON, self.onUserChoice)
            btn_sizer.Add(btn, flag=wx.ALL, border=8)
        
        
        panel.SetBackgroundColour(OUTER_BG)
        
        main_sizer = wx.BoxSizer(wx.VERTICAL)
       
        title_sizer = wx.BoxSizer(wx.HORIZONTAL)
        title_sizer.AddStretchSpacer()
        title_sizer.Add(title, 1, wx.EXPAND)
        title_sizer.AddStretchSpacer()
        main_sizer.Add(title_sizer, 0, wx.EXPAND | wx.TOP, 20)
        main_sizer.Add(btn_sizer, 0, wx.ALIGN_CENTER | wx.TOP, 24)
        
        self.result.SetMinSize((420, 110))
        try:
            self.result.Wrap(300)
        except Exception:
            pass
        result_box = wx.StaticBox(container, label="Result")
        result_box_sizer = wx.StaticBoxSizer(result_box, wx.VERTICAL)
        result_box_sizer.Add(self.result, 0, wx.ALL | wx.ALIGN_CENTER, 8)
       
        main_sizer.Add(result_box_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 24)

        info = wx.StaticText(container, label="Choose your move and see who wins!", style=wx.ALIGN_CENTER)
        info.SetForegroundColour(INFO_COLOR)
        info_font = wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_NORMAL)
        info.SetFont(info_font)
        main_sizer.Add(info, 0, wx.ALIGN_CENTER | wx.TOP, 12)
        container.SetSizer(main_sizer)
        outer_sizer = wx.BoxSizer(wx.VERTICAL)
        outer_sizer.AddStretchSpacer()
        outer_sizer.Add(container, 0, wx.ALIGN_CENTER)
        outer_sizer.AddStretchSpacer()
        panel.SetSizer(outer_sizer)

        self.Centre()
        self.Show()
        # Bind to capture F11 and ESC for fullscreen toggling
        self.Bind(wx.EVT_CHAR_HOOK, self.on_key)
        if FULLSCREEN_ON_START:
            # Show as fullscreen (no title bar/decorations)
            self.ShowFullScreen(True)

    def onUserChoice(self, event):
        # buttons labels have emoji + label, but getResult expects just the label word
        label = event.GetEventObject().GetLabel()
        # label could be "✊ Rock" - keep both display and simplify for logic
        user_choice_display = label
        # For comparing values, extract the text after the emoji
        user_choice = label.split(maxsplit=1)[1]
        comp_choice_text = random.choice([c.split(maxsplit=1)[1] for c in choices])
        outcome = self.getResult(user_choice, comp_choice_text)
        # Add emoji and colored text in message as plain text
        if outcome == "It's a draw!":
            suffix = "🙃"
        elif outcome == "You win!":
            suffix = " 🎉"
        else:
            suffix = " 😢"
        # split the display name from the emoji for clarity in the 'You' line
        user_display_text = user_choice_display
        msg = f"You: {user_display_text}\nComputer: {comp_choice_text}\n{outcome}{suffix}"
        self.result.SetLabel(msg)
        # refresh layout to make sure the result area updates visual size and wrapping
        self.Layout()

    def on_key(self, event):
        """Toggle fullscreen with F11 and exit fullscreen with ESC.
        Bind to the frame's EVT_CHAR_HOOK to capture key presses at top level.
        """
        key = event.GetKeyCode()
        if key == wx.WXK_F11:
            # Toggle fullscreen
            self.ShowFullScreen(not self.IsFullScreen())
        elif key == wx.WXK_ESCAPE:
            # Escape exits fullscreen if active; otherwise pass through
            if self.IsFullScreen():
                self.ShowFullScreen(False)
            else:
                event.Skip()
        else:
            event.Skip()
    
    def getResult(self, user, comp):
        if user == comp:
            return "It's a draw!"
        win = (user == "Rock" and comp == "Scissors") or \
              (user == "Paper" and comp == "Rock") or \
              (user == "Scissors" and comp == "Paper")
        return "You win!" if win else "Computer wins!"

if __name__ == "__main__":
    app = wx.App()
    RockPaperScissors()
    app.MainLoop()
