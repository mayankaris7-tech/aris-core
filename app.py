# --- 3D THREE.JS HOLOGRAPHIC ARC REACTOR (MOUSE-REACTIVE TILT) ---
arc_reactor_3d_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { margin: 0; overflow: hidden; background: transparent; }
        #canvas3d { width: 100%; height: 260px; display: block; cursor: crosshair; }
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
        renderer.setPixelRatio(window.devicePixelRatio);
        container.appendChild(renderer.domElement);

        // Core Group for reactive tilting
        const reactorGroup = new THREE.Group();
        scene.add(reactorGroup);

        // Holographic Outer Rings
        const ringGeo1 = new THREE.TorusGeometry(2.5, 0.04, 16, 100);
        const ringMat1 = new THREE.MeshBasicMaterial({ color: 0x00f3ff, wireframe: true });
        const ring1 = new THREE.Mesh(ringGeo1, ringMat1);
        reactorGroup.add(ring1);

        const ringGeo2 = new THREE.TorusGeometry(1.9, 0.06, 16, 80);
        const ringMat2 = new THREE.MeshBasicMaterial({ color: 0x0284c7, wireframe: true });
        const ring2 = new THREE.Mesh(ringGeo2, ringMat2);
        reactorGroup.add(ring2);

        // Central Power Core
        const coreGeo = new THREE.IcosahedronGeometry(0.9, 1);
        const coreMat = new THREE.MeshBasicMaterial({ color: 0x38bdf8, wireframe: true });
        const core = new THREE.Mesh(coreGeo, coreMat);
        reactorGroup.add(core);

        // Quantum Dust / Sparks
        const particleGeo = new THREE.BufferGeometry();
        const particleCount = 220;
        const posArray = new Float32Array(particleCount * 3);
        for(let i = 0; i < particleCount * 3; i++) {
            posArray[i] = (Math.random() - 0.5) * 8;
        }
        particleGeo.setAttribute('position', new THREE.BufferAttribute(posArray, 3));
        const particleMat = new THREE.PointsMaterial({ size: 0.04, color: 0x00f3ff });
        const particles = new THREE.Points(particleGeo, particleMat);
        reactorGroup.add(particles);

        camera.position.z = 6;

        // Mouse Telemetry Tracking
        let mouseX = 0;
        let mouseY = 0;
        let targetX = 0;
        let targetY = 0;

        window.addEventListener('mousemove', (event) => {
            const rect = container.getBoundingClientRect();
            mouseX = ((event.clientX - rect.left) / container.clientWidth) * 2 - 1;
            mouseY = -(((event.clientY - rect.top) / container.clientHeight) * 2 - 1);
        });

        // Animation Loop with Smooth Damping
        function animate() {
            requestAnimationFrame(animate);

            // Autonomous self-rotation
            ring1.rotation.z += 0.01;
            ring2.rotation.z -= 0.015;
            core.rotation.y += 0.02;
            particles.rotation.y += 0.003;

            // Interactive dynamic tilt
            targetX = mouseX * 0.8;
            targetY = mouseY * 0.8;
            reactorGroup.rotation.y += (targetX - reactorGroup.rotation.y) * 0.06;
            reactorGroup.rotation.x += (-targetY - reactorGroup.rotation.x) * 0.06;

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
