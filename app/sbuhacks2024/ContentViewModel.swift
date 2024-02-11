import Foundation
import Combine

class ContentViewModel: ObservableObject {
    @Published var outputText: String = ""

    func fetchGeneratedText(prompt: String) {
        let session = URLSession(configuration: .default)
        let urlString = "http://localhost:5000/generate-text" // Make sure this URL points to the correct endpoint
        guard let url = URL(string: urlString) else {
            DispatchQueue.main.async {
                self.outputText = "Error: Bad URL"
            }
            return
        }
        
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        
        
        request.addValue("application/json", forHTTPHeaderField: "Content-Type")
        
        let body: [String: Any] = ["prompt": prompt]
        request.httpBody = try? JSONSerialization.data(withJSONObject: body, options: [])
        
        let task = session.dataTask(with: request) { [weak self] data, response, error in
            if let error = error {
                DispatchQueue.main.async {
                    self?.outputText = "Network error: \(error.localizedDescription)"
                }
                return
            }

            guard let data = data else {
                DispatchQueue.main.async {
                    self?.outputText = "Error: No data received"
                }
                return
            }

            do {
                let decodedResponse = try JSONDecoder().decode(GeneratedTextResponse.self, from: data)
                DispatchQueue.main.async {
                    self?.outputText = decodedResponse.message
                }
            } catch {
                DispatchQueue.main.async {
                    self?.outputText = "Error decoding JSON: \(error.localizedDescription)"
                }
            }
        }
        task.resume()
    }
}

struct GeneratedTextResponse: Decodable {
    let message: String
}
