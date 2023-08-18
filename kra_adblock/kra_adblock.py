from krita import *
import re

supportedKritaVersions = [
    '5.1', # Tested with: Krita 5.1.5
    '5.2', # Tested with: Krita 5.2.0 beta2
    '5.3', # Tested with: Krita 5.3.0 prealpha
]

blocklistDefinitions = [
    (['5.1', '5.2', '5.3'], [
        # Community links
        (QLabel,      'gettingStartedLink' ),
        (QLabel,      'helpTitleLabel'     ),
        (QLabel,      'kritaWebsiteLink'   ),
        (QLabel,      'manualLink'         ),
        (QLabel,      'poweredByKDELink'   ),
        (QLabel,      'sourceCodeLink'     ),
        (QLabel,      'supportKritaLink'   ),
        (QLabel,      'userCommunityLink'  ),
        (QPushButton, 'gettingStartedIcon' ),
        (QPushButton, 'kdeIcon'            ),
        (QPushButton, 'kritaWebsiteIcon'   ),
        (QPushButton, 'sourceCodeIcon'     ),
        (QPushButton, 'supportKritaIcon'   ),
        (QPushButton, 'userCommunityIcon'  ),
        (QPushButton, 'userManualIcon'     ),
        # News panel
        (QWidget,     'widgetRight'        ),
        # Bottom text advert
        (QLabel,      'labelSupportText'   ),
    ]),
    (['5.2', '5.3'], [
        # Top banner advert
        (QLabel,      'lblBanner'          ),
        # Off-placed shortcut labels
        (QLabel,      'newFileLinkShortcut'),
        (QLabel,      'openFileShortcut'   ),
    ]),
]

class KraAdblock(Extension):
    def __init__(self, parent):
        super().__init__(parent)

    def setup(self):
        self.blocklistVersion = re.search(r'(\d+\.\d+)\..*', Krita.instance().version()).group(1)

        if not self.blocklistVersion in supportedKritaVersions:
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
            for blocklistVersions, blocklist in blocklistDefinitions:
                if self.blocklistVersion in blocklistVersions:
                    for widgetType, widgetName in blocklist:
                        if widget := window.qwindow().findChild(widgetType, widgetName):
                            widget.setVisible(False)
