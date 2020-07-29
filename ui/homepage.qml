import QtQuick 2.9
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.4
import org.kde.kirigami 2.12 as Kirigami
import QtGraphicalEffects 1.0
import Mycroft 1.0 as Mycroft

Mycroft.Delegate {
    id: wikiHomeDelegate
    skillBackgroundSource: Qt.resolvedUrl("books.png")
    leftPadding: 0
    rightPadding: 0
    bottomPadding: 0
    topPadding: 0
    
    ListModel {
        id: sampleModel
        ListElement {example: "How old is Clint Eastwood ?"}
        ListElement {example: "Where was Abraham Lincoln born ?"}
        ListElement {example: "What is the occupation of Linus Torvalds ?"}
        ListElement {example: "What is Albert Einstein date of birth ?"}
        ListElement {example: "What is Abraham Lincoln date of death ?"}
        ListElement {example: "Who is the spouse of Steve Jobs ?"}
    }
    
    Rectangle {
        id: headerBar
        anchors.top: parent.top
        anchors.left: parent.left
        anchors.right: parent.right
        height: Kirigami.Units.gridUnit * 2
        color: "#303030"
        layer.enabled: true
        layer.effect: DropShadow {
            transparentBorder: true
            horizontalOffset: 0
            verticalOffset: 2
        }
        
        RowLayout {
            width: parent.width
            height: parent.height
            anchors.verticalCenter: parent.verticalCenter
            
            ToolButton {
                Kirigami.Theme.colorSet: Kirigami.Theme.Button
                Layout.preferredWidth: Kirigami.Units.iconSizes.medium
                Layout.preferredHeight: Kirigami.Units.iconSizes.medium
                Layout.alignment: Qt.AlignLeft | Qt.AlignVCenter
                
                contentItem: Kirigami.Icon {
                    anchors.centerIn: parent
                    source: "arrow-left"
                }
                
                onClicked: {
                    wikiHomeDelegate.parent.backRequested()
                }
            }
            
            Kirigami.Heading {
                level: 2
                text: "Wikidata"
                Layout.fillWidth: true
                horizontalAlignment: Text.AlignHCenter
            }
        }
    }
    
    Rectangle {
        anchors.top: headerBar.bottom
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.bottom: parent.bottom
        color: Qt.rgba(0, 0, 0, 0.7)
        
        ColumnLayout {
            id: root
            anchors.fill: parent
            anchors.margins: Kirigami.Units.largeSpacing
            
            Kirigami.Heading {
                level: 2
                font.bold: true
                text: "What can it do" 
            }
            
            Label {
                Layout.fillWidth: true
                wrapMode: Text.WordWrap
                text: "Get current, historic facts & information about a person from Wikidata"
            }
            
            Item {
                Layout.preferredHeight: Kirigami.Units.largeSpacing
            }
            
            Kirigami.Heading {
                level: 2
                font.bold: true
                text: "Examples"
            }
                                    
            ListView {
                id: skillExampleListView
                Layout.fillWidth: true
                Layout.fillHeight: true
                focus: true
                clip: true
                model: sampleModel
                spacing: Kirigami.Units.smallSpacing
                delegate: Kirigami.AbstractListItem {
                    id: rootCard
                    
                    background: Kirigami.ShadowedRectangle {
                        color: rootCard.pressed ? Kirigami.Theme.highlightColor : Kirigami.Theme.backgroundColor
                        radius: Kirigami.Units.smallSpacing
                    }
                    
                    contentItem: Label {
                            anchors.left: parent.left
                            anchors.right: parent.right
                            anchors.rightMargin: Kirigami.Units.largeSpacing
                            anchors.leftMargin: Kirigami.Units.largeSpacing
                            wrapMode: Text.WordWrap
                            verticalAlignment: Text.AlignVCenter
                            elide: Text.ElideRight
                            color: Kirigami.Theme.textColor
                            text: "Hey Mycroft, " + model.example
                    }

                    onClicked: {
                        Mycroft.MycroftController.sendText(model.example)
                    }
                }
            }
        }
    }
}
