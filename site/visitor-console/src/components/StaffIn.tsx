import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { FieldValues, useForm } from "react-hook-form";
import { yupResolver } from "@hookform/resolvers/yup";
import * as yup from "yup";
import PageCard from "./PageCard";
import { api_endpoint } from "../library/constants";

const schema = yup.object({
  username: yup.string().required("Please enter your username."),
  password: yup.string().required("Please enter your password."),
});

interface StaffInProps {
  setAuthenticated: (value: boolean) => void;
}

const StaffIn = ({ setAuthenticated }: StaffInProps) => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm({
    resolver: yupResolver(schema),
  });

  const onSubmit = handleSubmit((data: FieldValues) =>
    signinUser(data as FormData)
  );

  interface FormData {
    username: string;
    password: string;
  }

  const signinUser = (formData: FormData) => {
    const body = {
      username: formData.username,
      password: formData.password,
    };

    setLoading(true);

    /*
    // Send the credentials to your authentication endpoint for validation
    fetch(`${api_endpoint}/authenticate`, {
      method: "post",
      body: JSON.stringify(body),
    }).then((response) => {
      setLoading(false);
      if (response.ok) {
        setLoading(false);
        setAuthenticated(true);
      } else {
        navigate("/error");
      }
    });
    */
    setLoading(false);
    setAuthenticated(true);
  };

  if (loading) {
    return <PageCard title="Staff Sign-In" subtitle="Loading..." />;
  }

  return (
    <PageCard title="Staff Sign-In">
      <form onSubmit={onSubmit}>
        <div className="form-group mb-3">
          <label htmlFor="username" className="form-label">
            Username
          </label>
          <input
            id="username"
            type="text"
            className="form-control"
            placeholder="Username"
            {...register("username")}
          />
          {errors.username && (
            <span className="form-text text-danger d-block">
              {errors.username.message}
            </span>
          )}
        </div>
        <div className="form-group mb-3">
          <label htmlFor="password" className="form-label">
            Password
          </label>
          <input
            id="password"
            type="password"
            className="form-control"
            placeholder="Password"
            {...register("password")}
          />
        </div>
        <div className="d-flex justify-content-between">
          <button type="submit" className="btn btn-secondary mr-5">
            Sign In
          </button>
        </div>
      </form>
    </PageCard>
  );
};

export default StaffIn;
