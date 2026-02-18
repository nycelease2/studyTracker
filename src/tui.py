#!/bin/python

from textual import on, log
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
                ("d", "delete_session", "Delete Session"),
                ("r", "refresh", "Refresh"),
                ("e", "edit", "Edit Session")]

    def action_edit(self):
        list_view = self.query_one("#session_list")
        if list_view.index is None:
            log.info("none selected")
            return

        self.push_screen(EditSession(list_view.index))

    async def action_delete_session(self):
        list_view = self.query_one("#session_list")
        if list_view.index is None:
            log.info("none selected")
            return

        def check_result(result):
            if result == "yes":
                # Use the index captured when the action was first triggered
                self.manager.delete(list_view.index)
                self.manager.save()
                self.refreshScreen()

        self.push_screen(ConfirmDeletion(), check_result)

    def action_add_session(self):
        self.push_screen(AddSessionScreen())

    def action_refresh(self):
        self.refreshScreen()

    def refreshScreen(self):
        list_view = self.query_one("#session_list")
        list_view.clear()

        self.manager.load()
        for session_dict in self.manager.session_data:
            list_view.append(ListItem(Static(session_dict["title"])))


    def on_mount(self):
        self.manager = SessionManager("sessions.json")
        self.manager.load()

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
    def __init__(self):
        super().__init__()

    def compose(self):

        yield Vertical(
                Static("Are you sure you want to delete this session?\n"),
                ListView(ListItem(Static("Yes")), ListItem(Static("No")), id="options"), id = "dialog_container"
            )

    async def on_list_view_selected(self, event):
        if event.index == 0:
            log.debug("deleting")
            self.dismiss("yes")
        else:
            self.dismiss("no")


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
        
        try:
            self.newSession = Session(start, end, title, desc)
            self.app.manager.add(self.newSession)
        except:
            log.error("something was wrong")

        self.app.manager.save()
        self.app.refreshScreen()
        self.app.pop_screen()

class EditSession(Screen):
    def __init__(self, index):
        super().__init__()
        self.index = index
        # We don't touch self.app here!

    def compose(self) -> ComposeResult:
        yield Header()
        yield Label("Editing Session", id="title_label")
        yield Vertical(
            # Using 'value' instead of 'placeholder' so the text is editable
            Input(id="edit_title"),
            Input(id="edit_start"),
            Input(id="edit_end"),
            Input(id="edit_desc"),
            Button("Save", variant="success", id="save_btn"),
            id="edit_form"
        )
        yield Footer()

    def on_mount(self):
        """Now that the screen is mounted, we can safely access self.app."""
        session = self.app.manager.session_data[self.index]
        
        # Populate the inputs with existing data
        self.query_one("#edit_title").value = session["title"]
        self.query_one("#edit_start").value = session["start_time"]
        self.query_one("#edit_end").value = session["end_time"]
        self.query_one("#edit_desc").value = session["description"]

    @on(Input.Submitted)
    @on(Button.Pressed)
    def save(self, event: Button.Pressed):
            # 1. Grab the new values
            new_data = {
                "title": self.query_one("#edit_title").value,
                "start_time": self.query_one("#edit_start").value,
                "end_time": self.query_one("#edit_end").value,
                "description": self.query_one("#edit_desc").value,
            }
            
            # 2. Update your manager (assuming you have an update method)
            self.app.manager.session_data[self.index].update(new_data)
            self.app.manager.save()
            
            # 3. Return to main screen and refresh
            self.app.pop_screen()
            self.app.refreshScreen()


if __name__ == "__main__":
    app = ScheduleApp()
    app.run()


