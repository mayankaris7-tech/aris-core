
import streamlit.components.v1 as components

# --- 3D THREE.JS HOLOGRAPHIC ARC REACTOR COMPONENT ---
arc_reactor_3d_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { margin: 0; overflow: hidden; background: transparent; }
        #canvas3d { width: 100%; height: 260px; display: block; }
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
</head>
<body>
    <div id="canvas3d"></div>
    <script>
        const container = document.getElementById('canvas3d');
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(50, container.clientWidth / container.clientHeight, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
        renderer.setSize(container.clientWidth, container.clientHeight);
        container.appendChild(renderer.domElement);

        // Core Glowing Rings
        const ringGeo1 = new THREE.TorusGeometry(2.5, 0.05, 16, 100);
        const ringMat1 = new THREE.MeshBasicMaterial({ color: 0x00f3ff, wireframe: true });
        const ring1 = new THREE.Mesh(ringGeo1, ringMat1);
        scene.add(ring1);

        const ringGeo2 = new THREE.TorusGeometry(1.8, 0.08, 16, 80);
        const ringMat2 = new THREE.MeshBasicMaterial({ color: 0x0284c7, wireframe: true });
        const ring2 = new THREE.Mesh(ringGeo2, ringMat2);
        scene.add(ring2);

        // Arc Core (Icosahedron Wireframe)
        const coreGeo = new THREE.IcosahedronGeometry(1.0, 1);
        const coreMat = new THREE.MeshBasicMaterial({ color: 0x38bdf8, wireframe: true });
        const core = new THREE.Mesh(coreGeo, coreMat);
        scene.add(core);

        // Surrounding Energy Particles
        const particleGeo = new THREE.BufferGeometry();
        const particleCount = 200;
        const posArray = new Float32Array(particleCount * 3);
        for(let i = 0; i < particleCount * 3; i++) {
            posArray[i] = (Math.random() - 0.5) * 8;
        }
        particleGeo.setAttribute('position', new THREE.BufferAttribute(posArray, 3));
        const particleMat = new THREE.PointsMaterial({ size: 0.04, color: 0x00f3ff });
        const particles = new THREE.Points(particleGeo, particleMat);
        scene.add(particles);

        camera.position.z = 6;

        // Animation Loop
        function animate() {
            requestAnimationFrame(animate);
            ring1.rotation.z += 0.01;
            ring1.rotation.x += 0.005;
            ring2.rotation.z -= 0.015;
            ring2.rotation.y += 0.008;
            core.rotation.y += 0.02;
            core.rotation.x -= 0.01;
            particles.rotation.y += 0.002;
            renderer.render(scene, camera);
        }
        animate();

        window.addEventListener('resize', () => {
            camera.aspect = container.clientWidth / container.clientHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(container.clientWidth, container.clientHeight);
        });
    </script>
</body>
</html>
"""

# App interface me jahan header khatam hota hai wahan bas yeh call karein:
components.html(arc_reactor_3d_html, height=270)
