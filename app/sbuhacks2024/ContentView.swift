import SwiftUI

struct ContentView: View {
    @State private var inputText: String = ""
    @ObservedObject var viewModel = ContentViewModel()
    @State private var showSecondView = false
    @State private var showDrainView = false
    
    @State private var isPressed = false
    @State private var isSpinning = false

    var body: some View {
        VStack {
            if (showDrainView) {
                Text("braindrAIn")
                    .font(.headline)
                    .padding()
                Spacer()
                Text(viewModel.outputText)
                    .padding()
                    .lineSpacing(10)
                Spacer()
                HStack {
                    TextField("Guess the word at the first blank!", text: $inputText)
                        .textFieldStyle(RoundedBorderTextFieldStyle())
                        .submitLabel(.go)
                        .onSubmit {
                            viewModel.outputText = "LOADING..."
                            viewModel.fetchGeneratedText(prompt: inputText)
                            inputText = ""
                        }
                        .padding(.leading, 20) // Add padding to the left
                        .padding(.trailing, 8) // Existing right padding
                    Button(action: {
                        viewModel.outputText = "LOADING..."
                        viewModel.fetchGeneratedText(prompt: inputText)
                        inputText = ""
                    }) {
                        Image(systemName: "arrow.right.circle.fill")
                            .resizable()
                            .frame(width: 30, height: 30)
                            .foregroundColor(.blue)
                    }
                    .padding(.trailing, 17)
                }
                .onChange(of: viewModel.outputText) { newValue in
                    if newValue == "Send a new prompt to play again!" {
                        showDrainView = false
                        isPressed = false
                        isSpinning.toggle()
                    }
                }
                Spacer()
            }
            else if (showSecondView) {
                Text("braindrAIn")
                    .font(.headline)
                    .padding()
                Spacer()
                Text(viewModel.outputText)
                    .padding()
                    .lineSpacing(10)
                    .scaleEffect(isSpinning ? 0.1 : 1)
                    .rotationEffect(.degrees(isSpinning ? 360 : 0))
                    .animation(Animation.linear(duration: 2.5), value: isSpinning)
                Spacer()
                HStack {
                    Text("Tell me about")
                        .padding()
                    TextField("(ex: cheese, NYC, penguins)", text: $inputText)
                        .textFieldStyle(RoundedBorderTextFieldStyle())
                        .submitLabel(.go)
                        .onSubmit {
                            viewModel.outputText = "LOADING..."
                            viewModel.fetchGeneratedText(prompt: inputText)
                            inputText = ""
                        }
                        .padding(-15)
                        .padding(.trailing, 20)
                    Button(action: {
                        viewModel.outputText = "LOADING..."
                        viewModel.fetchGeneratedText(prompt: inputText)
                        inputText = ""
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
                    viewModel.fetchGeneratedText(prompt: "COMPLETEDRAIN")
                    isSpinning.toggle()
                    inputText = ""
                    DispatchQueue.main.asyncAfter(deadline: .now() + 2.5) {
                        isPressed.toggle()
                        showDrainView = true
                    }
                }) {
                    Text("DRAIN KEY WORDS")
                        .bold()
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
                Spacer()
                Spacer()
                Image("braindrainlogo")
                    .resizable()
                    .scaledToFit()
                    .frame(width: 400, height: 400)
                Text("braindrAIn")
                    .font(.system(size: 50))
                    .padding(.top, -50)
                Text("Test your memory!")
                    .font(.headline)
                HStack {
                    Text("Let's learn about")
                        .padding()
                    TextField("(ex: cheese, NYC, penguins)", text: $inputText)
                        .textFieldStyle(RoundedBorderTextFieldStyle())
                        .submitLabel(.go)
                        .onSubmit {
                            viewModel.outputText = "LOADING..."
                            showSecondView = true
                            viewModel.fetchGeneratedText(prompt: inputText) // Trigger text fetching on submit
                        }
                        .padding(-15)
                        .padding(.trailing, 20)
                    Button(action: {
                        viewModel.outputText = "LOADING..."
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
                Spacer()
                Spacer()
                Spacer()
                Text("Created by Bryan Wong and Jason Wu")
            }
        }
    }
}


struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}

