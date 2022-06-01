from .base import Block
from dominate import tags
from dominate.util import raw


class MeshBlock(Block):
    def __init__(self):
        pass

    def update_doc(self, doc, data):
        style = raw(
            """
            .three-div {
                width: 200px;
                height: 200px;
            }
            #three_canvas {
                position: absolute;
                left: 0;
                width: 100%;
                height: 100%;
            }
        """
        )
        style_elem = None
        for head_child in doc.head.children:
            if isinstance(head_child, tags.style):
                style_elem = head_child
                break
        if style_elem is None:
            style_elem = tags.style()
            doc.head.add(style_elem)
        style_elem.add(style)

        pre_body = []

        pre_body += [
            tags.canvas(id="three_canvas")
        ]  # TODO: What if other block also want things on top?

        pre_body += [
            raw(
                """
                <script async src="https://unpkg.com/es-module-shims@1.3.6/dist/es-module-shims.js"></script>
            """
            )
        ]

        pre_body += [
            raw(
                """
                <script type="importmap">
                    {
                        "imports": {
                            "three": "https://unpkg.com/three@0.141.0/build/three.module.js"
                        }
                    }
                </script>
            """
            )
        ]

        three_script = tags.script(type="module")
        three_script.add(
            raw(
                """
                import * as THREE from "three";
                import {OBJLoader} from "https://unpkg.com/three@0.141.0/examples/jsm/loaders/OBJLoader";

                const geometry = new THREE.BoxGeometry(1, 1, 1);
                const material = new THREE.MeshBasicMaterial({color: 0x00ff00});
                function obj_laoder_callback(obj_mesh, scene) {
                    scene.add(obj_mesh);
                }

                function load_objects(objectPath, scene) {
                    console.log(`Loading object from ${objectPath}`);
                    const loader = new OBJLoader();
                    loader.load(
                        objectPath,
                        (obj_mesh) => {
                            obj_laoder_callback(obj_mesh, scene);
                        },
                        null, null, null
                    )
                }
                
                const scenes = [];
                function create_three_cell(cell_id, objectPath) {
                    const scene = new THREE.Scene();
                    const cell = document.getElementById(cell_id);
                    scene.userData.element = cell;
                    
                    const camera = new THREE.PerspectiveCamera(50, 1, 1, 10);
                    camera.position.z = 2;
                    scene.userData.camera = camera;

                    const light = new THREE.DirectionalLight( 0xffffff, 0.5 );
                    light.position.set( 1, 1, 1 );
                    scene.add( light ); 

                    load_objects(objectPath, scene);

                    // scene.add(new THREE.Mesh(geometry, material));
                    return scene;
                }

                const canvas = document.getElementById("three_canvas");
                const renderer = new THREE.WebGLRenderer({canvas: canvas, antialias: true});
                renderer.setClearColor( 0xffffff, 1 );
                renderer.setPixelRatio( window.devicePixelRatio );

                function animate() {
                    render()
                    requestAnimationFrame(animate);
                }
                animate();

                function updateSize() {

                    const width = canvas.clientWidth;
                    const height = canvas.clientHeight;

                    if ( canvas.width !== width || canvas.height !== height ) {
                        renderer.setSize( width, height, false );
                    }
                }

                function render() {
                    updateSize();
                    canvas.style.transform = `translateY(${window.scrollY}px)`;
                    renderer.setClearColor( 0xffffff );
                    renderer.setScissorTest( false );
                    renderer.clear();

                    renderer.setClearColor( 0xe0e0e0 );
                    renderer.setScissorTest( true );
                    scenes.forEach(function (scene) {
                        if (scene.children.length >= 2) {
                            scene.children[1].rotation.x += 0.01;
                            scene.children[1].rotation.y += 0.01;
                        }
                        
                        const element = scene.userData.element;
                        const rect = element.getBoundingClientRect();
                        const width = rect.right - rect.left;
                        const height = rect.bottom - rect.top;
                        const left = rect.left;
                        const bottom = renderer.domElement.clientHeight - rect.bottom;
                        renderer.setViewport(left, bottom, width, height);
                        renderer.setScissor(left, bottom, width, height);
                        const camera = scene.userData.camera;
                        renderer.render(scene, camera);
                    });
                }
            """
            )
        )

        for cell, cell_id, mesh_path in data:
            three_script.add(
                raw(
                    f"""
                    scenes.push(create_three_cell("{cell_id}", "{mesh_path}"));
                    """
                )
            )
            with cell:
                tags.attr(cls="three-div")
        pre_body += [three_script]
        doc.body.children = pre_body + doc.body.children
        return doc
