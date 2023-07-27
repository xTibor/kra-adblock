from krita import *
import re

widgetBlockList = {
    '5.1': [
        # Tested with: Krita 5.1.5
        (QLabel,            'gettingStartedLink' ),
        (QLabel,            'helpTitleLabel'     ),
        (QLabel,            'kritaWebsiteLink'   ),
        (QLabel,            'labelSupportText'   ),
        (QLabel,            'manualLink'         ),
        (QLabel,            'poweredByKDELink'   ),
        (QLabel,            'sourceCodeLink'     ),
        (QLabel,            'supportKritaLink'   ),
        (QLabel,            'userCommunityLink'  ),
        (QPushButton,       'gettingStartedIcon' ),
        (QPushButton,       'kdeIcon'            ),
        (QPushButton,       'kritaWebsiteIcon'   ),
        (QPushButton,       'sourceCodeIcon'     ),
        (QPushButton,       'supportKritaIcon'   ),
        (QPushButton,       'userCommunityIcon'  ),
        (QPushButton,       'userManualIcon'     ),
        (QWidget,           'widgetRight'        ),
    ],
    '5.2': [
        # Tested with: Krita 5.2.0 beta1
        # https://invent.kde.org/graphics/krita/-/merge_requests/1853
        (QLabel,            'labelSupportText'   ),
        (QLabel,            'lblBanner'          ),
        (QWidget,           'widgetCenter'       ),
        (QWidget,           'widgetRight'        ),
    ],
    '5.3': [
        # Tested with: Krita 5.3.0 prealpha
        (QLabel,            'gettingStartedLink' ),
        (QLabel,            'helpTitleLabel'     ),
        (QLabel,            'kritaWebsiteLink'   ),
        (QLabel,            'labelSupportText'   ),
        (QLabel,            'lblBanner'          ),
        (QLabel,            'manualLink'         ),
        (QLabel,            'newFileLinkShortcut'),
        (QLabel,            'openFileShortcut'   ),
        (QLabel,            'poweredByKDELink'   ),
        (QLabel,            'sourceCodeLink'     ),
        (QLabel,            'supportKritaLink'   ),
        (QLabel,            'userCommunityLink'  ),
        (QPushButton,       'gettingStartedIcon' ),
        (QPushButton,       'kdeIcon'            ),
        (QPushButton,       'kritaWebsiteIcon'   ),
        (QPushButton,       'sourceCodeIcon'     ),
        (QPushButton,       'supportKritaIcon'   ),
        (QPushButton,       'userCommunityIcon'  ),
        (QPushButton,       'userManualIcon'     ),
        (QWidget,           'widgetRight'        ),
    ],
}

class KraAdblock(Extension):
    def __init__(self, parent):
        super().__init__(parent)

    def setup(self):
        self.blockListVersion = re.search(r'(\d+\.\d+)\..*', Krita.instance().version()).group(1)

        if not self.blockListVersion in widgetBlockList:
            print("kra-adblock: Unsupported Krita version")
            return

        appNotifier = Krita.instance().notifier()
        appNotifier.windowCreated.connect(self.blockAdsAllWindows)
        appNotifier.setActive(True)

        self.blockAdsAllWindows()

    def createActions(self, window):
        pass

    def blockAdsAllWindows(self):
        for window in Krita.instance().windows():
            for widgetType, widgetName in widgetBlockList[self.blockListVersion]:
                if widget := window.qwindow().findChild(widgetType, widgetName):
                    widget.setVisible(False)
