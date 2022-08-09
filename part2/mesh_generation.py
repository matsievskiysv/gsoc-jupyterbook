from mpi4py import MPI
import gmsh


def generate_mesh(lmbda, order):
    if MPI.COMM_WORLD.rank == 0:
        gmsh.model.add("helmholtz_domain")

        # Set the mesh size
        gmsh.option.setNumber("Mesh.CharacteristicLengthFactor", 2*lmbda)


        # Add scatterers
        c1 = gmsh.model.occ.addCircle(0.0, -1.1*lmbda, 0.0, lmbda/2)
        gmsh.model.occ.addCurveLoop([c1], tag=c1)
        gmsh.model.occ.addPlaneSurface([c1], tag=c1)

        c2 = gmsh.model.occ.addCircle(0.0, 1.1*lmbda, 0.0, lmbda/2)
        gmsh.model.occ.addCurveLoop([c2], tag=c2)
        gmsh.model.occ.addPlaneSurface([c2], tag=c2)

        # Add domain
        r0 = gmsh.model.occ.addRectangle(
            -5*lmbda, -5*lmbda, 0.0, 10*lmbda, 10*lmbda)
        inclusive_rectangle, _ = gmsh.model.occ.fragment(
            [(2, r0)], [(2, c1), (2, c2)])

        gmsh.model.occ.synchronize()

        # Add physical groups
        gmsh.model.addPhysicalGroup(2, [c1, c2], tag=1)
        gmsh.model.addPhysicalGroup(2, [r0], tag=2)

        # Generate mesh
        gmsh.model.mesh.generate(2)
        gmsh.model.mesh.setOrder(order)
        gmsh.model.mesh.optimize("HighOrder")

        return gmsh.model
