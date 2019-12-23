import QtQuick 2.9
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.4
import org.kde.kirigami 2.8 as Kirigami
import Mycroft 1.0 as Mycroft

Mycroft.Delegate {
    skillBackgroundSource: Qt.resolvedUrl("books.png")
        
    ColumnLayout {
        id: root
        anchors.fill: parent
        
        Item {
            height: Kirigami.Units.gridUnit * 5
        }
        
        ListModel {
            id: sampleModel
            ListElement {example: "How old is Clint Eastwood"}
            ListElement {example: "Where was Abraham Lincoln born"}
            ListElement {example: "What is the occupation of Linus Torvalds"}
            ListElement {example: "What is Albert Einstein date of birth"}
            ListElement {example: "What is Abraham Lincoln date of death"}
            ListElement {example: "What is Steve Jobs spouse name"}
        }

        Rectangle {
            Layout.fillWidth: true
            Layout.fillHeight: true
            color: Qt.rgba(Kirigami.Theme.backgroundColor.r, Kirigami.Theme.backgroundColor.g, Kirigami.Theme.backgroundColor.b, 0.8)
            
            ColumnLayout {
                anchors.fill: parent
                
                RowLayout {
                    Layout.leftMargin: Kirigami.Units.largeSpacing
                    Layout.fillWidth: true
                    
                    Image {
                        Layout.preferredHeight: Kirigami.Units.iconSizes.medium
                        Layout.preferredWidth: Kirigami.Units.iconSizes.medium
                        source: "https://d2.alternativeto.net/dist/icons/wikidata_151529.png?width=128&height=128&mode=crop&upscale=false"
                    }
                    
                    Kirigami.Heading {
                        level: 1
                        Layout.leftMargin: Kirigami.Units.largeSpacing
                        text: "Wikidata" 
                    }
                }
                Kirigami.Heading {
                    level: 3
                    Layout.leftMargin: Kirigami.Units.largeSpacing
                    text: "Get current and historic facts & information about a person from Wikidata." 
                }
                
                Kirigami.Separator {
                    Layout.fillWidth: true
                    Layout.preferredHeight: 1
                }
                
                Rectangle {
                    Layout.fillWidth: true
                    Layout.preferredHeight: hd2.contentHeight + Kirigami.Units.largeSpacing
                    color: Kirigami.Theme.linkColor
                    
                    Kirigami.Heading {
                        id: hd2
                        level: 3
                        width: parent.width
                        anchors.left: parent.left
                        anchors.leftMargin: Kirigami.Units.largeSpacing
                        anchors.verticalCenter: parent.verticalCenter
                        text: "Some examples to get you started, try asking..."
                    }
                }
                                
                ListView {
                    id: skillExampleListView
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    keyNavigationEnabled: true
                    focus: true
                    highlightFollowsCurrentItem: true
                    snapMode: ListView.SnapToItem
                    model: sampleModel
                    delegate: Kirigami.BasicListItem {
                        id: rootCard
                        reserveSpaceForIcon: false
                        label: "Hey Mycroft, " + model.example
                    }
                }
            }
        }
        
        Item {
            height: Kirigami.Units.gridUnit * 12
        }
    }
}
