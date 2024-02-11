import SwiftUI

struct ContentView: View {
    @State private var inputText: String = ""
    @ObservedObject var viewModel = ContentViewModel()

    var body: some View {
        VStack {
            Spacer()
            Text(viewModel.outputText)
                .padding()
                .lineSpacing(10)
            Spacer()
            Spacer()
            Spacer()
            HStack {
                TextField("Let's Learn!", text: $inputText)
                    .textFieldStyle(RoundedBorderTextFieldStyle())
                    .submitLabel(.go)
                    .onSubmit {
                        viewModel.fetchGeneratedText(prompt: inputText)
                    }
                    .padding()
                Button(action: {
                    viewModel.fetchGeneratedText(prompt: inputText)
                }) {
                    Image(systemName: "arrow.right.circle.fill")
                        .resizable()
                        .frame(width:30, height: 30)
                        .foregroundColor(.blue)
                }
                .padding(.leading, -10)
                .padding(.trailing, 12)
            }
            
            Spacer()
        }
        .navigationBarTitle("Your Title Here", displayMode: .inline)
    }
    
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
