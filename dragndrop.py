# /// script
# requires-python = ">=3.9"
# dependencies = [
#     "pyqt5",
# ]
# ///
from PyQt5 import QtCore, QtGui, QtWidgets

class DropBear(QtWidgets.QWidget):
    def __init__(self, parent=None, geom=(400, 400, 800, 800)):
        super().__init__(parent)
        self.setGeometry(*geom)
        self.setAcceptDrops(True)
        self.label = QtWidgets.QLabel("drop file here...", wordWrap=True)
        self.image = QtWidgets.QLabel("<image here>")
        self.sourcecode = QtWidgets.QTextEdit()
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.image)
        layout.addWidget(self.sourcecode)
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
        if ev.mimeData().hasFormat("image/png") or ev.mimeData().hasImage():
            # TODO: something here, not getting pictures when trying this out
            ev.acceptProposedAction()
        elif ev.mimeData().hasUrls():
            urls = ev.mimeData().urls()
            # load just the first for now
            if (ok := self.loadURL(urls[0])):
                url, image, text = ok
                self.label.setText(url)
                self.image.setPixmap(QtGui.QPixmap.fromImage(image))
                self.sourcecode.setText(text)
                ev.acceptProposedAction()

    def loadURL(self, url: "QtCore.QUrl", text_mimetype="text/x-python"):
        try:
            image = QtGui.QImage(url.toLocalFile())
            text = image.text(text_mimetype)
            # alternative:
            # from PIL import Image
            # with Image.open(url.toLocalFile()) as im:
            #     text = im.text.get(text_mimetype, "")
        except OSError:  # , PIL.UnidentifiedImageError
            return None
        else:
            return str(url), image, text


app = QtWidgets.QApplication([])

win = DropBear()
win.show()

app.exec()
