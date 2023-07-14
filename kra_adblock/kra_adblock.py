from krita import *

widgetBlockList = [
    # Krita 5.1.5
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
    # Krita 5.2.x
    # https://invent.kde.org/graphics/krita/-/merge_requests/1853
    #(KisClickableLabel, 'lblBanner'         ),
]

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
        for window in Krita.instance().windows():
            for widgetType, widgetName in widgetBlockList:
                if widget := window.qwindow().findChild(widgetType, widgetName):
                    widget.setVisible(False)
