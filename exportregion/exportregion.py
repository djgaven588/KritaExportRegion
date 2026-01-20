# type: ignore
from krita import *
from PyQt5.QtWidgets import QWidget, QAction
from pprint import pprint
from functools import partial

# This is a combination of https://github.com/ollyisonit/krita-export-region and my (Destiny Hailstorm)'s efforts
# The original didn't support exporting a region with transparency, instead cropping it, while this handles it.
# I've never written a Krita plugin before, so I wish you luck future travelers

class ExportRegionExtension(Extension):
    def __init__(self, parent):
        super().__init__(parent)

    # If part of the document is selected, export the selection.
    # If nothing is selected, export everything in the current layer's bounding box.
    def export_region(self):
        # Ensure valid
        doc = Krita.instance().activeDocument()
        if not doc:
            show_message("No document is selected!")
            return

        selection = doc.selection()
        if not selection:
            show_message("No selection to export!")
            return

        # Setup doc
        export_doc = Krita.instance().createDocument(selection.width(), selection.height(), "Export Doc", "RGBA", doc.colorDepth(), doc.colorProfile(), doc.resolution())
        Krita.instance().activeWindow().addView(export_doc)
        Krita.instance().setActiveDocument(export_doc)

        # Remove existing nodes
        for layer in export_doc.topLevelNodes():
            layer.remove()

        # Copy data
        newNode = export_doc.createNode("Copy", "paintlayer")
        ba = doc.pixelData(selection.x(), selection.y(), selection.width(), selection.height())
        newNode.setPixelData(ba, 0, 0, selection.width(), selection.height())

        export_doc.rootNode().addChildNode(newNode, None)

        # Finish
        export_doc.refreshProjection()
        export_doc.waitForDone()

        Krita.instance().action("file_export_file").trigger()
        export_doc.setModified(False)
        Krita.instance().setActiveDocument(doc)
        export_doc.close()

    def show_message(text):
        dialog = QDialog()
        dialog.setWindowTitle("!")
        label = QLabel(text)
        layout = QVBoxLayout()
        layout.addWidget(label)
        dialog.setLayout(layout)
        dialog.setModal(True)
        dialog.exec_()

    def setup(self):
        pass

    def createActions(self, window):
        export_region_action = window.createAction(
            "hailstorm_export_region", "Export Region...", "file"
        )
        export_region_action.triggered.connect(self.export_region)
        QTimer.singleShot(
            0, partial(self.moveAction, export_region_action, window.qwindow())
        )

    # Take the existing export_region action and move it to be after file_export in the file menu
    def moveAction(self, action, qwindow):
        menu_bar = qwindow.menuBar()
        file_menu_action = next(
            (a for a in menu_bar.actions() if a.objectName() == "file"), None
        )
        if file_menu_action:
            file_menu = file_menu_action.menu()
            for file_action in file_menu.actions():
                if file_action.objectName() == "file_export_advanced":
                    file_menu.removeAction(action)
                    file_menu.insertAction(file_action, action)


Krita.instance().addExtension(ExportRegionExtension(Krita.instance()))
