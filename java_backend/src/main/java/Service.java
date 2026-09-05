package com.sih.planner;

import org.springframework.stereotype.Service;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

@Service
public class Service {

    private static final String PYTHON_ENGINE_URL = "http://127.0.0.1:8000/api/v1/optimize";
    private final HttpClient httpClient = HttpClient.newHttpClient();

    public String callPythonEngine(String jsonPayload) {
        try {
            HttpRequest request = HttpRequest.newBuilder()
                    .uri(URI.create(PYTHON_ENGINE_URL))
                    .header("Content-Type", "application/json")
                    .POST(HttpRequest.BodyPublishers.ofString(jsonPayload))
                    .build();

            HttpResponse<String> response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());
            return response.body();
        } catch (Exception e) {
            return "{\"error\": \"Failed to reach Python service\"}";
        }
    }
}