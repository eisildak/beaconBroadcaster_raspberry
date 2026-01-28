import SwiftUI

@main
struct BeaconBroadcasterApp: App {
    @StateObject private var bluetoothManager = BluetoothManager()
    @StateObject private var beaconStore = BeaconStore()
    
    var body: some Scene {
        WindowGroup {
            ContentView()
                .environmentObject(bluetoothManager)
                .environmentObject(beaconStore)
                .frame(minWidth: 800, minHeight: 600)
        }
        .windowStyle(.hiddenTitleBar)
        .windowResizability(.contentSize)
        .commands {
            CommandGroup(replacing: .newItem) {}
            CommandMenu("Beacon") {
                Button("Add Beacon") {
                    beaconStore.showingAddBeacon = true
                }
                .keyboardShortcut("n", modifiers: .command)
                
                Divider()
                
                Button("Stop All Broadcasting") {
                    bluetoothManager.stopAllBroadcasts()
                }
                .keyboardShortcut(".", modifiers: .command)
            }
        }
        
        Settings {
            SettingsView()
                .environmentObject(bluetoothManager)
        }
    }
}
