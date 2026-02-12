#!/bin/python

from operator import index
from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.getters import query_one
from textual.widgets import Footer, Header, Static, ListView, ListItem
from main import SessionManager

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

    BINDINGS = [("a", "increment", "Add Session")]


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

if __name__ == "__main__":
    app = ScheduleApp()
    app.run()



