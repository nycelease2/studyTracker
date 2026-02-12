#!/bin/python

from operator import index
from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.widgets import Footer, Header, Static, ListView, ListItem
from main import SessionManager

class ScheduleApp(App):
    """A Textual app to manage a scheduler."""


    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Horizontal(
            ListView(id = "session_list"),
            Static("Title: ", id="title"),
            Static("Start Time: ", id="start_time"),
            Static("End Time: ", id="end_time"),
            Static("Total Time: ", id="total_time"),
            Static("Description: ", id="desc")
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
        self.query_one("#title").update(f"Title: {title_print}")


if __name__ == "__main__":
    app = ScheduleApp()
    app.run()
