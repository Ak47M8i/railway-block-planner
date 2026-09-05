package com.sih.planner;

import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api")
@CrossOrigin(origins = "*") // Allows web requests from frontend
public class Controller {

    private final Service pythonService;

    public Controller(Service pythonService) {
        this.pythonService = pythonService;
    }

    @PostMapping("/schedule")
    public String generateSchedule(@RequestBody String requestJson) {
        // Receives request from Web Frontend and sends it to Python FastAPI Engine
        return pythonService.callPythonEngine(requestJson);
    }
}