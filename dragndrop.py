# /// script
# requires-python = ">=3.9"
# dependencies = [
#     "pyqt5",
# ]
# ///
from PyQt5 import QtWidgets

class DropBear(QtWidgets.QWidget):
    def __init__(self, parent=None, geom=(400, 400, 800, 800)):
        super().__init__(parent)
        self.setGeometry(*geom)
        self.setAcceptDrops(True)
        self.label = QtWidgets.QLabel("drop file here...", wordWrap=True)
        self.fp = QtWidgets.QLabel("", wordWrap=True)
        self.content = QtWidgets.QLabel("", wordWrap=True)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.fp)
        layout.addWidget(self.content)
        self.setLayout(layout)

    def dragEnterEvent(self, ev):
        self.label.setText(str(ev.mimeData().formats()))
        if ev.mimeData().hasFormat("image/png"):
            ev.acceptProposedAction()
        elif ev.mimeData().hasFormat("text/uri-list"):
            ev.acceptProposedAction()

    def dragLeaveEvent(self, ev):
        self.label.setText("drop file here...")

    def dropEvent(self, ev):
        if ev.mimeData().hasFormat("image/png"):
            ev.acceptProposedAction()
        elif ev.mimeData().hasFormat("text/uri-list"):
            # TODO: maybe just text()?
            # please no spaces in file names
            # files = ev.mimeData().text().split(" ")
            # print(files)
            b = bytes(ev.mimeData().data("text/uri-list"))
            # XXX: doesn't handle #comment lines lol
            urls = b.decode("latin-1").split("\r\n")
            self.fp.setText("<ul><li>" + "<li>".join(u for u in urls if u) + "</ul>")
            # TODO: load file and only accept if image/png
            ev.acceptProposedAction()


app = QtWidgets.QApplication([])

win = DropBear()
win.show()

app.exec()
