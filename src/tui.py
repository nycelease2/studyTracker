#!/bin/python

from textual import on
from operator import index
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.getters import query_one
from textual.screen import ModalScreen, Screen
from textual.widgets import Footer, Header, OptionList, Static, ListView, ListItem, Input, Button, Label
from main import SessionManager, Session

class ScheduleApp(App):
    """A Textual app to manage a scheduler."""


    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Horizontal(
            ListView(id = "session_list"),
            Static("Title: \nStart Time: \nEnd Time: \nTotal Duration: \nDescription: ", id="details"),
        )
        yield Footer()

    BINDINGS = [("a", "add_session", "Add Session"), 
                ("d", "delete_session", "Delete Session")]

    async def action_delete_session(self):
        list_view = self.query_one("#session_list")
        if list_view.index is None:
            return

        result = await self.push_screen(ConfirmDeletion(list_view.index))

        if result == "yes":
            del self.manager.session_data[list_view.index]
            self.manager.save()
            self.refreshScreen()


    def action_add_session(self):
        self.push_screen(AddSessionScreen())


    def refreshScreen(self):
        list_view = self.query_one("#session_list")
        list_view.clear()

        for session_dict in self.manager.session_data:
            list_view.append(ListItem(Static(session_dict["title"])))


    def on_mount(self):
        self.manager = SessionManager("sessions.json")
        self.manager.load()
        self.count = len(self.manager.session_data)

        list_view = self.query_one("#session_list")

        for session_dict in self.manager.session_data:
            title = session_dict["title"]
            list_view.append(ListItem(Static(title)))


    def on_list_view_selected(self, event):
        title_print = self.manager.session_data[event.index]["title"]
        startT_print = self.manager.session_data[event.index]["start_time"]
        endT_print = self.manager.session_data[event.index]["end_time"]
        durationT_print = self.manager.from_dict(self.manager.session_data[event.index]).total_time
        desc_print = self.manager.session_data[event.index]["description"]

        self.query_one("#details").update(f"Title: {title_print}\nStart Time: {startT_print}\nEnd Time: {endT_print}\nTotal Duration: {durationT_print}\nDescription: {desc_print}")


    CSS = """
    #session_list {
        width: 1fr;
    }

    #details {
        width: 2fr;
        padding: 1 2;
    }
    """

class ConfirmDeletion(ModalScreen):
    def __init__(self, session_index):
        super().__init__()
        self.choice = None
        self.session_index = session_index

    def compose(self):

        yield Vertical(
                Static("Are you sure you want to delete this session?\n"),
                ListView(ListItem(Static("[Yes]")), ListItem(Static("[No]")), id="options"), id = "dialog_container"
                )

        


    def on_list_view_selected(self, event):
        if event.index == 0:
            self.choice = "yes"
        else:
            self.choice = "no"

        self.dismiss(self.choice)

    CSS = """

        #dialog_container {
    width: 40%;       /* small box */
    height: auto;     
    align: center middle; /* center in terminal */
    border: round yellow;
    padding: 1 2;
    background: #222; /* optional dark background */
}


    """

class AddSessionScreen(Screen):
    def compose(self):
        yield Header()
        yield Static("Add New Session")
        yield Vertical(
                Input(placeholder="Title", id="title"),
                Input(placeholder="Start time (YYYY-MM-DDTHH:MM:SS)", id="start"),
                Input(placeholder="End time (YYYY-MM-DDTHH:MM:SS)", id="end"),
                Input(placeholder="Description", id="desc"),
                Button("Save")
                )
        yield Footer()

    @on(Button.Pressed)
    @on(Input.Submitted)
    def save_session(self) -> None:
        title = self.query_one("#title", Input).value
        start = self.query_one("#start", Input).value
        end = self.query_one("#end", Input).value
        desc = self.query_one("#desc", Input).value
        
        self.newSession = Session(start, end, title, desc)

        self.app.manager.add(self.newSession)
        self.app.manager.save()
        self.app.refreshScreen()
        self.app.pop_screen()

if __name__ == "__main__":
    app = ScheduleApp()
    app.run()



