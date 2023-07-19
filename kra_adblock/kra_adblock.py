from krita import *
import re

widgetBlockList = {
    '5.1': [
        (QLabel,            'gettingStartedLink'),
        (QLabel,            'helpTitleLabel'    ),
        (QLabel,            'kritaWebsiteLink'  ),
        (QLabel,            'labelSupportText'  ),
        (QLabel,            'manualLink'        ),
        (QLabel,            'poweredByKDELink'  ),
        (QLabel,            'sourceCodeLink'    ),
        (QLabel,            'supportKritaLink'  ),
        (QLabel,            'userCommunityLink' ),
        (QPushButton,       'gettingStartedIcon'),
        (QPushButton,       'kdeIcon'           ),
        (QPushButton,       'kritaWebsiteIcon'  ),
        (QPushButton,       'sourceCodeIcon'    ),
        (QPushButton,       'supportKritaIcon'  ),
        (QPushButton,       'userCommunityIcon' ),
        (QPushButton,       'userManualIcon'    ),
        (QWidget,           'widgetRight'       ),
    ],
    '5.2': [
        # https://invent.kde.org/graphics/krita/-/merge_requests/1853
        (QLabel,            'labelSupportText'  ),
        (QLabel,            'lblBanner'         ),
        (QWidget,           'widgetCenter'      ),
        (QWidget,           'widgetRight'       ),
    ],
}

class KraAdblock(Extension):
    def __init__(self, parent):
        super().__init__(parent)

    def setup(self):
        appNotifier = Krita.instance().notifier()
        appNotifier.windowCreated.connect(self.blockAdsAllWindows)
        appNotifier.setActive(True)

        self.blockAdsAllWindows()

    def createActions(self, window):
        pass

    def blockAdsAllWindows(self):
        versionFull = Krita.instance().version()
        versionMajMin = re.search(r'(\d+\.\d+)\..*', versionFull).group(1)

        for window in Krita.instance().windows():
            for widgetType, widgetName in widgetBlockList[versionMajMin]:
                if widget := window.qwindow().findChild(widgetType, widgetName):
                    widget.setVisible(False)
