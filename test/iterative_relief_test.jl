using Test
include("../skrelief/IterativeRelief.jl")


# Test functionality with continuous features.
@testset "IterativeRelief - Continuous Features" begin
    data = rand(1000, 10)
    for idx1 = 1:size(data, 2) - 1
        for idx2 = idx1+1:size(data, 2)
            target = Int64.(data[:, idx1] .> data[:, idx2])
            weights = IterativeRelief.iterative_relief(data, target, f_type="continuous")
            @test all(weights[idx1] .>= weights[(1:end .!= idx1) .& (1:end .!= idx2)])
            @test all(weights[idx2] .>= weights[(1:end .!= idx1) .& (1:end .!= idx2)])
        end
    end
end


# Test functionality with discrete features.
@testset "IterativeRelief - Discrete Features" begin
    data = rand([0, 1, 2, 3], 1000, 10)
    for idx1 = 1:size(data, 2) - 1
        for idx2 = idx1+1:size(data, 2)
            target = Int64.(data[:, idx1] .> data[:, idx2])
            weights = IterativeRelief.iterative_relief(data, target, f_type="discrete")
            @test all(weights[idx1] .>= weights[(1:end .!= idx1) .& (1:end .!= idx2)])
            @test all(weights[idx2] .>= weights[(1:end .!= idx1) .& (1:end .!= idx2)])
        end
    end
end


# Test exceptions.
@testset "IterativeRelief - Exceptions" begin
    data = rand([0, 1, 2, 3], 1000, 10)
    target = Int64.(data[:, 1] .> data[:, 2])
    @test_throws DomainError IterativeRelief.iterative_relief(data, target, f_type="something_else")
end

