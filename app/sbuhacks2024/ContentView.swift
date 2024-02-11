import SwiftUI

struct ContentView: View {
    @State private var inputText: String = ""
    @ObservedObject var viewModel = ContentViewModel()
    @State private var showSecondView = false
    @State private var showDrainView = false
    
    @State private var isPressed = false // Tracks the button's state
    
    var body: some View {
        VStack {
            if (showDrainView) {
                
            }
            else if (showSecondView) {
                // Second view content
                Spacer()
                Text(viewModel.outputText)
                    .padding()
                    .lineSpacing(10)
                Spacer()
                Spacer()
                HStack {
                    Text("Tell me about")
                        .padding()
                    TextField("(ex: cheese, NYC, penguins)", text: $inputText)
                        .textFieldStyle(RoundedBorderTextFieldStyle())
                        .submitLabel(.go)
                        .onSubmit {
                            viewModel.fetchGeneratedText(prompt: inputText)
                        }
                        .padding(-15)
                        .padding(.trailing, 20)
                    Button(action: {
                        viewModel.fetchGeneratedText(prompt: inputText)
                    }) {
                        Image(systemName: "arrow.right.circle.fill")
                            .resizable()
                            .frame(width:30, height: 30)
                            .foregroundColor(.blue)
                    }
                    .padding(.trailing, 12)
                }
                .padding(.bottom, 20)
                Button(action: {
                    DispatchQueue.main.asyncAfter(deadline: .now() + 1) {
                        isPressed.toggle()
                        showDrainView = true
                    }
                }) {
                    Text("DRAIN")
                        .frame(minWidth: 0, maxWidth: .infinity)
                        .padding()
                        .foregroundColor(isPressed ? .black : .white)
                        .background(isPressed ? Color.white : Color.black)
                        .cornerRadius(10)
                        .overlay(RoundedRectangle(cornerRadius: 10)
                            .stroke(Color.black, lineWidth: isPressed ? 2 : 0)
                        )
                }
                .padding(.horizontal)
                Spacer()
            } else {
                // First view content
                Image(systemName: "brain") // Your actual logo here
                    .resizable()
                    .scaledToFit()
                    .frame(width: 200, height: 200)
                Text("braindrAIn")
                    .font(.system(size: 50))
                Text("Let's test your memory!")
                    .font(.headline)
                HStack {
                    Text("Tell me about")
                        .padding()
                    TextField("(ex: cheese, NYC, penguins)", text: $inputText)
                        .textFieldStyle(RoundedBorderTextFieldStyle())
                        .submitLabel(.go)
                        .onSubmit {
                            showSecondView = true
                            viewModel.fetchGeneratedText(prompt: inputText) // Trigger text fetching on submit
                        }
                        .padding(-15)
                        .padding(.trailing, 20)
                    Button(action: {
                        showSecondView = true
                        viewModel.fetchGeneratedText(prompt: inputText) // Also fetch text when button is pressed
                    }) {
                        Image(systemName: "arrow.right.circle.fill")
                            .resizable()
                            .frame(width:30, height: 30)
                            .foregroundColor(.blue)
                    }
                    .padding(.trailing, 12)
                }
            }
        }
    }
}


struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}

