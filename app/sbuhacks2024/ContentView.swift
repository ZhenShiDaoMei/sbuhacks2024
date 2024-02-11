import SwiftUI

struct ContentView: View {
    @State private var inputText: String = ""
    @ObservedObject var viewModel = ContentViewModel()

    var body: some View {
        VStack {
            TextField("Enter some text", text: $inputText)
                .textFieldStyle(RoundedBorderTextFieldStyle())
                .padding()

            Button(action: {
                viewModel.fetchGeneratedText(prompt: inputText)
            }) {
                Text("Generate")
                    .frame(minWidth: 0, maxWidth: .infinity, minHeight: 0, maxHeight: 50)
                    .background(Color.blue)
                    .foregroundColor(.white)
                    .cornerRadius(10)
                    .padding(.horizontal)
            }

            Text(viewModel.outputText)
                .padding()
            
            Spacer()
        }
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
