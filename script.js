// script.js

console.log("Hello World page script loaded!");

// You can add more JavaScript interactions here if needed.

console.log("Demonstrating Git workflow."); // Added for Git example 

import * as THREE from 'three';

// Get the container element
const container = document.getElementById('three-container');

if (container) {
    // Scene setup
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0xf0f0f0); // Light grey background

    // Camera setup (Perspective Camera)
    const fov = 75; // Field of View
    const aspect = container.clientWidth / container.clientHeight; // Aspect Ratio
    const near = 0.1; // Near clipping plane
    const far = 1000; // Far clipping plane
    const camera = new THREE.PerspectiveCamera(fov, aspect, near, far);
    camera.position.z = 5; // Move camera back so we can see the cube

    // Renderer setup (WebGL Renderer)
    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(container.clientWidth, container.clientHeight);

    // Add the renderer's canvas element to the container
    container.appendChild(renderer.domElement);

    // --- Cube Creation ---
    const geometry = new THREE.BoxGeometry(1, 1, 1); // Width, height, depth
    const material = new THREE.MeshBasicMaterial({ color: 0x0077ff }); // Blue color
    const cube = new THREE.Mesh(geometry, material);
    scene.add(cube); // Add the cube to the scene
    // --- End Cube Creation ---

    // --- Animation Loop ---
    function animate() {
        requestAnimationFrame(animate); // Request the next frame

        // Rotate the cube
        cube.rotation.x += 0.01;
        cube.rotation.y += 0.01;

        // Render the scene
        renderer.render(scene, camera);
    }
    animate(); // Start the animation loop
    // --- End Animation Loop ---

    // Handle window resize
    window.addEventListener('resize', () => {
        const newAspect = container.clientWidth / container.clientHeight;
        camera.aspect = newAspect;
        camera.updateProjectionMatrix();
        renderer.setSize(container.clientWidth, container.clientHeight);
    });

} else {
    console.error('Could not find the #three-container element.');
} 