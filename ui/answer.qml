import QtQuick.Layouts 1.4
import QtQuick 2.4
import QtQuick.Controls 2.0
import org.kde.kirigami 2.4 as Kirigami

import Mycroft 1.0 as Mycroft

Mycroft.ProportionalDelegate {
    skillBackgroundSource: sessionData.imgLink
    skillBackgroundColorOverlay: "#88000000"
    
    ColumnLayout {
        id: grid
        Layout.fillWidth: true
        width: parent.width
        spacing: Kirigami.Units.largeSpacing * 1.25
        
        Item {
            height: Kirigami.Units.largeSpacing * 2
        }
        
        Image {
            id: img
            fillMode: Image.PreserveAspectCrop
            Layout.alignment: Qt.AlignHCenter
            Layout.preferredWidth: Kirigami.Units.gridUnit * 10
            Layout.preferredHeight: Kirigami.Units.gridUnit * 10
            source: sessionData.imgLink
        }
        Mycroft.AutoFitLabel {
            id: answer
            Layout.fillWidth: true
            Layout.preferredHeight: proportionalGridUnit * 20
            Layout.alignment: Qt.AlignHCenter
            wrapMode: Text.WordWrap
            font.capitalization: Font.Capitalize
            font.family: "Noto Sans"
            font.weight: Font.Bold
            text: sessionData.answerData
        }
    }
}
